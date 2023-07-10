import pandas as pd
import argparse

from ATE import Samplerun


def run_sim_job(batch_idx, in_dir, out_dir):
    in_file = "%s/batch%d_in.csv" % (in_dir, batch_idx)
    out_file = "batch%d_out.csv" % batch_idx

    in_data = pd.read_csv(in_file)

    run = Samplerun(no_docker=True)
    run.perform_sample(out_file=out_file, out_dir=out_dir, param_values=in_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, help="Batch index")
    parser.add_argument("--in-dir", type=str, help="Directory containing input files")
    parser.add_argument("--out-dir", type=str, help="Directory for output files")
    args = parser.parse_args()

    run_sim_job(args.batch, args.in_dir, args.out_dir)
