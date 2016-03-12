# -*- coding: utf-8 -*-

def get_database_genes(session, database_name):
    return session.query(Database, Gene.locus_id).join(DatabaseGene).join(Gene).filter(Database.name == database_name).all()
