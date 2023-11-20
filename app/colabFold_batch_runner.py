import logging
import os
import sys
from pathlib import Path
from sys import version_info

sys.path.insert(0, os.path.abspath('.'))
from colabfold.batch import get_queries, run
from colabfold.utils import setup_logging

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s %(lineno)d: %(message)s",
    datefmt="%m-%d %H:%M:%S",
)
python_version = f"{version_info.major}.{version_info.minor}"
logger.info("python_version %s", python_version)


default_data_dir = Path("/mnt/sda/alphafold/af_data")

model_type = "alphafold2_multimer_v2"  # @param ["auto", "alphafold2_ptm", "alphafold2_multimer_v1", "alphafold2_multimer_v2", "alphafold2_multimer_v3"]
# @markdown - if `auto` selected, will use `alphafold2_ptm` for monomer prediction and `alphafold2_multimer_v3` for complex prediction.

msa_mode = "mmseqs2_uniref_env"  # @param ["MMseqs2 (UniRef+Environmental)", "MMseqs2 (UniRef only)","single_sequence","custom"]
pair_mode = (
    "unpaired_paired"  # @param ["unpaired_paired","paired","unpaired"] {type:"string"}
)
# @markdown - "unpaired_paired" = pair sequences from same species + unpaired MSA, "unpaired" = seperate MSA for each chain, "paired" - only use paired sequences.
num_models = 5  # @param [1,2,3,4,5] {type:"raw"}

num_recycles = "auto"  # @param [1,3,6,12,24,48] {type:"raw"}
recycle_early_stop_tolerance = "auto"  # @param ["auto", "0.0", "0.5", "1.0"]
# @markdown - if `auto` selected, will use 20 recycles if
# `model_type=alphafold2_multimer_v3` (with tol=0.5), all else 3 recycles (with tol=0.0).
num_recycles = None if num_recycles == "auto" else int(num_recycles)
pairing_strategy = "greedy"
recycle_early_stop_tolerance = (
    None
    if recycle_early_stop_tolerance == "auto"
    else float(recycle_early_stop_tolerance)
)

stop_at_score = 100.0  # @param {type:"string"}
# @markdown - early stop computing models once score > threshold (avg. plddt for "structures" and ptmscore for "complexes")
use_custom_msa = False
# A nice design to control relaxed num to optimize the speed.
num_relax = 0

template_mode = "none" #@param ["none", "pdb100","custom"]
#@markdown - `none` = no template information is used. `pdb100` = detect templates in pdb100 (see [notes](#pdb100)). `custom` - upload and search own templates (PDB or mmCIF format, see [notes](#custom_templates))
use_templates = True  # @param {type:"boolean"}
keep_existing_results = True  # @param {type:"boolean"}
zip_results = False  # @param {type:"boolean"}
model_order = [1, 2, 3, 4, 5]  # [1, 2, 3, 4, 5]

if template_mode == "pdb100":
    use_templates = True
    custom_template_path = None
elif template_mode == "none":
    custom_template_path = None
    use_templates = False


# @markdown #### Save settings
dpi = 200  # @param {type:"integer"}
# @markdown - set dpi for image resolution

# @markdown #### Sample settings
max_msa = "auto"  # @param ["auto", "512:1024", "256:512", "64:128", "32:64", "16:32"]
num_seeds = 1
# @markdown -  decrease `max_msa` to increase uncertainity
use_dropout = False
if max_msa == "auto":
    max_msa = None

if "multimer" in model_type and max_msa is not None:
    use_cluster_profile = False
else:
    use_cluster_profile = True

set_cyclic_offset = True

run_test = 1
# test_cyclic_peptide and test_linear_monomer are mutually exclusive.
test_cyclic_peptide = 1
test_linear_monomer = 1
if run_test:
    if test_cyclic_peptide:
        root_input_dir = Path(
            "/mnt/nas/alphafold/af_input/tasks/cyclic_peptide/multimer-test"
        )
        test_file = "test-ENMPALCKK.fasta"
    elif test_linear_monomer:
        root_input_dir = Path(
            "/mnt/nas/alphafold/af_input/tasks/monomer_demo/short_peptides"
        )
        test_file = "alpha_helix_DTFGRCRRWWAALGACRR.fasta"
    input_dir = root_input_dir / test_file
else:
    root_input_dir = Path(
        "/mnt/nas/alphafold/af_input/tasks/cyclic_peptide/FGF5-all-pos2"
    )
    input_dir = root_input_dir
result_dir = (
    f"/mnt/nas/alphafold/af_out/cf_{Path(input_dir).stem}_cyclic_offset-{set_cyclic_offset}"  # @param {type:"string"}
)
Path(result_dir).mkdir(exist_ok=1, parents=1)

if "logging_setup" not in globals():
    setup_logging(Path(result_dir).joinpath("log.log"))
    logging_setup = True

queries, is_complex = get_queries(input_dir)
logger.info("is_complex %s, set_cyclic_offset %s use_cluster_profile %s", 
               is_complex, set_cyclic_offset, use_cluster_profile)
if run_test:
    logger.info("queries %s", queries)
if not is_complex:
    model_type = "alphafold2"


def main():
    """ """
    run(
        queries=queries,
        root_result_dir=result_dir,
        num_models=num_models,
        is_complex=is_complex,
        num_recycles=num_recycles,
        recycle_early_stop_tolerance=recycle_early_stop_tolerance,
        model_order=model_order,
        use_templates=use_templates,
        num_relax=num_relax,
        msa_mode=msa_mode,
        model_type=model_type,
        num_seeds=num_seeds,
        use_dropout=use_dropout,
        data_dir=default_data_dir,
        keep_existing_results=keep_existing_results,
        rank_by="auto",
        pair_mode=pair_mode,
        stop_at_score=stop_at_score,
        dpi=dpi,
        zip_results=zip_results,
        max_msa=max_msa,
        use_cluster_profile=use_cluster_profile,
        cyclic=set_cyclic_offset,
    )


if __name__ == "__main__":
    main()
