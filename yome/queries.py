# -*- coding: utf-8 -*-

from yome.models import Database, Gene, DatabaseGene

def get_database_genes(session, database_name):
    res = (session
           .query(Database, Gene.locus_id)
           .join(DatabaseGene)
           .join(Gene)
           .filter(Database.name == database_name))
    return [{database_name: x[0], gene_locus: x[1]} for x in res]
