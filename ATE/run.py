import numpy as np
import requests
import json
import docker
import pandas as pd
import time
import os

from .param import Parameter


class Samplerun:
    """
    Holds sampling methods and data for TBR docker run.
    """

    def __init__(
        self,
        no_docker=False,
        port=8080,
        container_name="openmcworkshop/find-tbr:latest",
        spin_up_time=5,
    ) -> None:
        """
        Collects sampling parameters
        """

        self.tbr = []
        self.no_docker = no_docker
        self.port = port
        self.request_url = (
            "http://localhost:%d/find_tbr_model_sphere_with_firstwall" % self.port
        )
        self.container_name = container_name
        self.docker = docker.from_env()
        self.container = None
        self.spin_up_time = spin_up_time

    def __del__(self) -> None:
        """
        Clean up docker container when the object is deleted.
        """
        # ensure that no container is left dangling
        self.stop_container()

    def start_container(self) -> None:
        """
        Start docker container with the TBR web service. Or attach to one if it's already running.
        """
        if self.no_docker:
            return

        if running_containers := [
            c
            for c in self.docker.containers.list()
            if self.container_name in c.image.tags
        ]:
            # do not start container if one is already running
            self.container = running_containers[0]
            print(f"Connecting to existing container {self.container.id}")
            return

        # key is container port, value is host port
        port_binding = {"8080/tcp": self.port}

        self.container = self.docker.containers.run(
            self.container_name, detach=True, remove=True, ports=port_binding
        )
        print(f"Started new container {self.container.id}")

        time.sleep(self.spin_up_time)

    def stop_container(self) -> None:
        """
        Stop docker container if it is running.
        """
        if self.container is None:
            return

        print(f"Stopping container {self.container.id}")
        self.container.stop()
        self.container = None

    def request_tbr(self, params):
        """
        Query the TBR web service and parse its output.
        """
        response = requests.get(self.request_url, params=params)
        return json.loads(response.content) if response.ok else None

    def perform_sample(
        self,
        out_file="default.csv",
        out_dir="output/",
        verb=True,
        param_values=None,
        domain=None,
        sampling_strategy=None,
        n_samples=None,
        progress_handler=None,
    ):
        """
        Interfaces with Docker to perform sample and saves to csv file
        """
        assert (
            n_samples is None or n_samples > 0
        ), "Input error, nonpositive number of samples."

        if param_values is None:
            param_values = domain.gen_data_frame(sampling_strategy, n_samples)
        else:
            n_samples = param_values.shape[0]

        results = pd.DataFrame(
            data={
                "tbr": [-1.0] * n_samples,
                "tbr_error": [-1.0] * n_samples,
                "sim_time": [-1.0] * n_samples,
            }
        )

        self.start_container()

        for i in range(n_samples):
            print("Performing sample %d of %d" % (i + 1, n_samples))
            tic = time.time()
            response = self.request_tbr(param_values.iloc[i].to_dict())
            toc = time.time()

            if response is not None:
                time_taken = toc - tic
                set_names = "tbr", "tbr_error", "sim_time"
                set_values = response["tbr"], response["tbr_error"], time_taken
                results.iloc[i][set_names] = set_values

            if verb:
                print(results.iloc[i]["tbr"])

            if progress_handler is not None:
                progress_handler(i, n_samples)

        merged = param_values.join(results)

        if out_file is not None:
            out_path = os.path.join(out_dir, out_file)
            merged.to_csv(out_path, index=False)

        self.stop_container()
        return merged
