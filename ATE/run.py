import numpy as np
import requests
import json
import docker
import pandas as pd
import time
import os

from .param import Parameter


class Samplerun:
    '''
    Holds sampling methods and data for TBR docker run.
    '''

    def __init__(self, n_samples, domain, sampling_strategy, port=8080, container_name="openmcworkshop/find-tbr:latest", spin_up_time=5):
        '''
        Collects sampling parameters
        '''
        assert (n_samples > 0), "Input error, nonpositive number of samples."
        self.n_samples = n_samples
        self.domain = domain
        self.sampling_strategy = sampling_strategy
        self.tbr = []
        self.port = port
        self.request_url = "http://localhost:%d/find_tbr_model_sphere_with_firstwall" % self.port
        self.container_name = container_name
        self.docker = docker.from_env()
        self.container = None
        self.spin_up_time = spin_up_time

    def __del__(self):
        # ensure that no container is left dangling
        self.stop_container()

    def start_container(self):
        running_containers = [c for c in self.docker.containers.list()
                              if self.container_name in c.image.tags]

        if len(running_containers) != 0:
            # do not start container if one is already running
            self.container = running_containers[0]
            print('Connecting to existing container %s' % self.container.id)
            return

        # key is container port, value is host port
        port_binding = {'8080/tcp': self.port}

        self.container = self.docker.containers.run(
            self.container_name, detach=True, remove=True, ports=port_binding)
        print('Started new container %s' % self.container.id)

        time.sleep(self.spin_up_time)

    def stop_container(self):
        if self.container is not None:
            print('Stopping container %s' % self.container.id)
            self.container.stop()
            self.container = None

    def request_tbr(self, params):
        response = requests.get(self.request_url, params=params)
        return json.loads(response.content) if response.ok else None

    def perform_sample(self, out_file="default.csv", out_dir="output/", verb=True):
        '''
        Interfaces with Docker to perform sample and saves to csv file
        '''

        param_values = self.domain.gen_data_frame(
            self.sampling_strategy, self.n_samples)
        results = pd.DataFrame(data={
            'tbr': [-1.] * self.n_samples,
            'tbr_error': [-1.] * self.n_samples,
            'sim_time': [-1.] * self.n_samples
        })

        self.start_container()

        for i in range(self.n_samples):
            print("Performing sample %d of %d" % (i + 1, self.n_samples))
            tic = time.time()
            response = self.request_tbr(param_values.iloc[i].to_dict())
            toc = time.time()

            if response is not None:
                time_taken = toc - tic
                results.iloc[i]['tbr',
                                'tbr_error',
                                'sim_time'] = response['tbr'], response['tbr_error'], time_taken

            if verb:
                print(results.iloc[i]['tbr'])

        merged = param_values.join(results)

        out_path = os.path.join(out_dir, out_file)
        merged.to_csv(out_path)

        self.stop_container()
