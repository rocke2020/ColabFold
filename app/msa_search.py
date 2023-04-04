import logging
import math
import shutil
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Union
import os, sys
sys.path.append(os.path.abspath('.'))
from utils.log_util import logger
from colabfold.batch import get_queries, msa_to_str
from colabfold.mmseqs.search import run_mmseqs, mmseqs_search_monomer, mmseqs_search_pair


def main():
    """  """
    parser = ArgumentParser()
    parser.add_argument(
        "query",
        type=Path,
        default='app/data/pos_complex_in_one_seq/1awr_C_I.fasta',
        help="fasta files with the queries.",
    )
    parser.add_argument(
        "dbbase",
        type=Path,
        default='/mnt/sdc/colabfold_db',
        help="The path to the database and indices you downloaded and created with setup_databases.sh",
    )
    parser.add_argument(
        "base", type=Path, help="Directory for the results (and intermediate files)",
        default='app/data/out'
    )
    parser.add_argument(
        "-s",
        type=int,
        default=8,
        help="mmseqs sensitivity. Lowering this will result in a much faster search but possibly sparser msas",
    )
    # dbs are uniref, templates and environmental
    # We normally don't use templates
    parser.add_argument(
        "--db1", type=Path, default=Path("uniref30_2202_db"), help="UniRef database"
    )
    parser.add_argument("--db2", type=Path, default=Path(""), help="Templates database")
    parser.add_argument(
        "--db3",
        type=Path,
        default=Path("colabfold_envdb_202108_db"),
        help="Environmental database",
    )
    # poor man's boolean arguments
    parser.add_argument("--use-env", type=int, default=1, choices=[0, 1])
    parser.add_argument("--use-templates", type=int, default=0, choices=[0, 1])
    parser.add_argument("--filter", type=int, default=1, choices=[0, 1])
    parser.add_argument(
        "--mmseqs",
        type=Path,
        default=Path("/home/qcdong/mmseqs/bin/mmseqs"),
        help="Location of the mmseqs binary",
    )
    parser.add_argument("--expand-eval", type=float, default=math.inf)
    parser.add_argument("--align-eval", type=int, default=10)
    parser.add_argument("--diff", type=int, default=3000)
    parser.add_argument("--qsc", type=float, default=-20.0)
    parser.add_argument("--max-accept", type=int, default=1000000)
    parser.add_argument("--db-load-mode", type=int, default=0)
    parser.add_argument("--threads", type=int, default=64)
    args = parser.parse_args()

    queries, is_complex = get_queries(args.query, None)

    queries_unique = []
    for job_number, (raw_jobname, query_sequences, a3m_lines) in enumerate(queries):
        # remove duplicates before searching
        query_sequences = (
            [query_sequences] if isinstance(query_sequences, str) else query_sequences
        )
        query_seqs_unique = []
        for x in query_sequences:
            if x not in query_seqs_unique:
                query_seqs_unique.append(x)
        query_seqs_cardinality = [0] * len(query_seqs_unique)
        for seq in query_sequences:
            seq_idx = query_seqs_unique.index(seq)
            query_seqs_cardinality[seq_idx] += 1

        queries_unique.append([raw_jobname, query_seqs_unique, query_seqs_cardinality])

    args.base.mkdir(exist_ok=True, parents=True)
    query_file = args.base.joinpath("query.fas")
    with query_file.open("w") as f:
        for job_number, (
            raw_jobname,
            query_sequences,
            query_seqs_cardinality,
        ) in enumerate(queries_unique):
            for seq in query_sequences:
                f.write(f">{raw_jobname}\n{seq}\n")

    run_mmseqs(
        args.mmseqs,
        ["createdb", query_file, args.base.joinpath("qdb"), "--shuffle", "0"],
    )
    with args.base.joinpath("qdb.lookup").open("w") as f:
        id = 0
        file_number = 0
        for job_number, (
            raw_jobname,
            query_sequences,
            query_seqs_cardinality,
        ) in enumerate(queries_unique):
            for seq in query_sequences:
                f.write(f"{id}\t{raw_jobname}\t{file_number}\n")
                id += 1
            file_number += 1

    mmseqs_search_monomer(
        mmseqs=args.mmseqs,
        dbbase=args.dbbase,
        base=args.base,
        uniref_db=args.db1,
        template_db=args.db2,
        metagenomic_db=args.db3,
        use_env=args.use_env,
        use_templates=args.use_templates,
        filter=args.filter,
        expand_eval=args.expand_eval,
        align_eval=args.align_eval,
        diff=args.diff,
        qsc=args.qsc,
        max_accept=args.max_accept,
        s=args.s,
        db_load_mode=args.db_load_mode,
        threads=args.threads,
    )
    if is_complex == True:
        mmseqs_search_pair(
            mmseqs=args.mmseqs,
            dbbase=args.dbbase,
            base=args.base,
            uniref_db=args.db1,
            s=args.s,
            db_load_mode=args.db_load_mode,
            threads=args.threads,
        )

        id = 0
        for job_number, (
            raw_jobname,
            query_sequences,
            query_seqs_cardinality,
        ) in enumerate(queries_unique):
            unpaired_msa = []
            paired_msa = None
            if len(query_seqs_cardinality) > 1:
                paired_msa = []
            for seq in query_sequences:
                with args.base.joinpath(f"{id}.a3m").open("r") as f:
                    unpaired_msa.append(f.read())
                args.base.joinpath(f"{id}.a3m").unlink()
                if len(query_seqs_cardinality) > 1:
                    with args.base.joinpath(f"{id}.paired.a3m").open("r") as f:
                        paired_msa.append(f.read())
                args.base.joinpath(f"{id}.paired.a3m").unlink()
                id += 1
            msa = msa_to_str(
                unpaired_msa, paired_msa, query_sequences, query_seqs_cardinality
            )
            args.base.joinpath(f"{job_number}.a3m").write_text(msa)

    query_file.unlink()    
    run_mmseqs(args.mmseqs, ["rmdb", args.base.joinpath("qdb")])
    run_mmseqs(args.mmseqs, ["rmdb", args.base.joinpath("qdb_h")])    

main()