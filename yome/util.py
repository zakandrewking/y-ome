from yome.models import (
    Gene,
    Knowledgebase,
    KnowledgebaseGene,
    KnowledgebaseFeature,
)

from datetime import timedelta
import pandas as pd
import re
from bs4 import BeautifulSoup
import matplotlib as mpl
import IPython
from IPython.core.magic import register_line_magic
from IPython.display import HTML


def create(session, query_class, commit=False, **kwargs):
    """Add a new row to the database and return.

    Arguments
    ---------

    session: The SQLAlchemy session.

    query_class: The class to query.

    commit: If True, then commit. Otherwise flush.

    """
    res = query_class(**kwargs)
    session.add(res)
    if commit:
        session.commit()
    else:
        session.flush()
    return res


def get_or_create(session, query_class, commit=False, **kwargs):
    """Query the query_class, filtering by the given keyword arguments. If no
    result is found, then add a new row to the database. Returns result of the
    query.

    Arguments
    ---------

    session: The SQLAlchemy session.

    query_class: The class to query.

    commit: If True, then commit. Otherwise flush.

    """
    res = session.query(query_class).filter_by(**kwargs).first()
    if res is not None:
        return res, True
    return create(session, query_class, commit=commit, **kwargs), False


def format_seconds(total_sec):
    """Format a time delta.

    """
    delt = timedelta(seconds=total_sec)
    days = delt.days
    hours, rem = divmod(delt.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    if seconds == 0:
        return '<1 s'
    s = '%s s' % seconds
    if minutes:
        s = '%d m ' % minutes + s
    if hours:
        s = '%d h ' % hours + s
    if days:
        s = '%d d ' % days + s
    return s


def to_df(query, cols=None):
    """Convert a SQLAlchemy query result to a DataFrame."""
    # Try to get column names
    if cols is None:
        cols = [x['name'] for x in query.column_descriptions]
    data = [{k: v for k, v in zip(cols, x)} for x in query]
    if len(data) == 0:
        return pd.DataFrame()
    return pd.DataFrame(data).loc[:, cols]


def apply_keyword(df, keyword, field, is_high):
    """Apply a keyword to the dataframe, and warn if it already has an
    annotation_quality. Give mismatches a 'tbd' label.

    """
    add, other = ('high', 'low') if is_high else ('low', 'high')
    df.loc[
        (df[field].str.contains(keyword, flags=re.IGNORECASE) &
         (df.annotation_quality != other)),
        'annotation_quality'
    ] = add
    # give mismatches a tbd label
    mismatch = df.loc[
        (df[field].str.contains(keyword, flags=re.IGNORECASE) &
         (df.annotation_quality == other)),
        'annotation_quality'
    ] = 'tbd'


def html_to_text(text):
    """Based on:

    https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python

    """
    soup = BeautifulSoup(text, 'lxml')
    return soup.get_text()


def report(session, locus_tag):
    """Print a report of all features for a gene"""
    quality_df = to_df(
        session.query(KnowledgebaseGene.annotation_quality,
                      Knowledgebase.name.label('knowledgebase_name'))
        .join(Knowledgebase)
        .join(Gene)
        .filter(Gene.locus_id == locus_tag)
    )

    features_df = to_df(
        session.query(Gene.locus_id,
                      KnowledgebaseGene.primary_name,
                      Knowledgebase.name.label('knowledgebase_name'),
                      KnowledgebaseFeature.feature_type,
                      KnowledgebaseFeature.feature)
        .join(KnowledgebaseGene)
        .join(Knowledgebase)
        .join(KnowledgebaseFeature)
        .filter(Gene.locus_id == locus_tag)
    )

    features_df = features_df.merge(quality_df, on='knowledgebase_name',
                                    how='outer')

    print(features_df.iloc[0, 0:2])

    def make_name(row):
        return f"{row['knowledgebase_name']} ({row['annotation_quality']})"
    features_df['knowledgebase_name'] = features_df.apply(make_name, axis=1)

    features_df = features_df.drop(
        ['locus_id', 'primary_name', 'annotation_quality'],
        axis=1,
    )
    features_df = features_df.set_index(['knowledgebase_name', 'feature_type'])
    s = features_df.style.set_properties(**{'text-align': 'left'})
    return HTML(s.render())


def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return round(val)


def scale_color(hexstr, scalefactor):
    """Scales a hex string by ``scalefactor``. Returns scaled hex string.

    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.

    >>> colorscale("#DF3C3C", .5)
    #6F1E1E
    >>> colorscale("#52D24F", 1.6)
    #83FF7E
    >>> colorscale("#4F75D2", 1)
    #4F75D2

    """

    hexstr = hexstr.strip('#')

    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    r = clamp(r * scalefactor)
    g = clamp(g * scalefactor)
    b = clamp(b * scalefactor)

    return '#%02x%02x%02x' % (r, g, b)

try:
    # Only run in the notebook environment
    @register_line_magic
    def mpl_setup(line):
        IPython.get_ipython().magic('pylab --no-import-all inline')

        try:
            import seaborn as sns
            sns.set(style="darkgrid")
        except ImportError:
            from warnings import warn
            warn('Seaborn not installed')

        mpl.rcParams['savefig.bbox'] = 'tight'
        mpl.rcParams['savefig.pad_inches'] = 0
        mpl.rcParams['text.usetex'] = False
        mpl.rcParams['lines.linewidth'] = 3
        mpl.rcParams['font.size'] = 15
        mpl.rcParams['axes.labelsize'] = 17
        mpl.rcParams['axes.titlesize'] = 17
        mpl.rcParams['xtick.labelsize'] = 15
        mpl.rcParams['ytick.labelsize'] = 15
        mpl.rcParams['legend.fontsize'] = 17
except NameError:
    pass
