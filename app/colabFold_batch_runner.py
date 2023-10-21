from pathlib import Path
import logging
from sys import version_info
from colabfold.batch import get_queries, run
from colabfold.utils import setup_logging


logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s %(filename)s %(lineno)d: %(message)s',
    datefmt='%m-%d %H:%M:%S')
python_version = f"{version_info.major}.{version_info.minor}"
logger.info('python_version %s', python_version)


default_data_dir = Path('/mnt/sda/alphafold/af_data')
msa_mode = "MMseqs2 (UniRef+Environmental)" #@param ["MMseqs2 (UniRef+Environmental)", "MMseqs2 (UniRef only)","single_sequence","custom"]
num_models = 5 #@param [1,2,3,4,5] {type:"raw"}
num_recycles = 6 #@param [1,3,6,12,24,48] {type:"raw"}
stop_at_score = 100 #@param {type:"string"}
#@markdown - early stop computing models once score > threshold (avg. plddt for "structures" and ptmscore for "complexes")
use_custom_msa = False
# A nice design to control relaxed num to optimize the speed.
num_relax = 2
use_amber = num_relax > 0 # that's when num_relax > 0, use_amber becomes True auto.
# use_amber = False #@param {type:"boolean"}
use_templates = True #@param {type:"boolean"}
keep_existing_results = True #@param {type:"boolean"}
zip_results = False #@param {type:"boolean"}
model_order = [1, ]  # [1, 2, 3, 4, 5]
# demo file

run_test_file = 1
if run_test_file:
    root_input_dir = Path('/mnt/nas/alphafold/af_input/tasks/monomer_demo/short_peptides')
    test_file = 'alpha_helix_DTFGRCRRWWAALGACRR.fasta'
    input_dir = root_input_dir / test_file
else:
    root_input_dir = Path('/mnt/nas/alphafold/af_input/tasks/peptides/anti_fungal_peptide')
    input_dir = root_input_dir
result_dir = f'/mnt/nas/alphafold/af_out/cf_{Path(input_dir).stem}' #@param {type:"string"}
Path(result_dir).mkdir(exist_ok=1, parents=1)
if 'logging_setup' not in globals():
    setup_logging(Path(result_dir).joinpath("log.log"))
    logging_setup = True


def main():
    """  """
    queries, is_complex = get_queries(input_dir)
    logger.info('is_complex %s', is_complex)
    run(
        queries=queries,
        result_dir=result_dir,
        use_templates=use_templates,
        use_amber=use_amber,
        msa_mode=msa_mode,
        model_type="alphafold2",
        num_models=num_models,
        num_recycles=num_recycles,
        model_order=model_order,
        is_complex=is_complex,
        data_dir=default_data_dir,
        keep_existing_results=keep_existing_results,
        rank_by="auto",
        pair_mode="unpaired+paired",
        stop_at_score=stop_at_score,
        zip_results=zip_results,
        num_seeds=5,
        num_relax=num_relax,
    )