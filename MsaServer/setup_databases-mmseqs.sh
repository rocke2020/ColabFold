WORKDIR="${1:-$(pwd)}"
echo ${WORKDIR}
cd "${WORKDIR}"

# if [ ! -f UNIREF30_READY ]; then
  # mmseqs tsv2exprofiledb "uniref30_2202" "uniref30_2202_db"
#   mmseqs createindex "uniref30_2202_db" tmp1 --remove-tmp-files 1
#   touch UNIREF30_READY
# fi
# mmseqs createindex "uniref30_2202_db" tmp1 --remove-tmp-files 1

# if [ ! -f COLABDB_READY ]; then
#   mmseqs tsv2exprofiledb "colabfold_envdb_202108" "colabfold_envdb_202108_db"
#   # TODO: split memory value for createindex?
#   mmseqs createindex "colabfold_envdb_202108_db" tmp2 --remove-tmp-files 1
#   touch COLABDB_READY
# fi
mmseqs createindex "colabfold_envdb_202108_db" tmp2 --remove-tmp-files 1
# if [ ! -f PDB_READY ]; then
#   mmseqs createdb pdb70_220313.fasta.gz pdb70_220313
#   mmseqs createindex pdb70_220313 tmp3 --remove-tmp-files 1
#   touch PDB_READY
# fi
