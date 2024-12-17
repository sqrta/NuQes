# NuQes

## Installation

```
git submodule add https://github.com/sqrta/funsearch.git
pip install -r requirements.txt
```

## Bivariate Bicycle Code Evaluation

We reuse the simulation software from [BCGMRY] Sergey Bravyi, Andrew Cross, Jay Gambetta, Dmitri Maslov, Patrick Rall, Theodore Yoder, High-threshold and low-overhead fault-tolerant quantum memory https://arxiv.org/abs/2308.07915. The original git repo is [here](https://github.com/sbravyi/BivariateBicycleCodes). The evaluation code is in the `BivariateBicycleCodes` folder

```
cd BivariateBicycleCodes
```

The simulation software consists of two python scripts:

set_decoder.py is the offline part of the decoder that constructs check matrices, syndrome measurement circuits, and decoding matrices for a particular quantum code. This computation can take a few minutes per code. All code data is saved to disk. One has to call decoder_setup.py only once for each combination (code, error rate, number of syndrome cycles).

decoder_run.py is the online part of the decoder that simulates error correction circuits. It relies on the software implementation of the Belief Propagation with the Ordered Statistics Decoder due to Joschka Roffe "LDPC: Python tools for low density parity check codes"

File naming: the working directory that contains decoder_setup.py and decoder_run.py must contain folders "TMP" and "CODE_n_k_d" for each code [[n,k,d]] to be simulated. Initially these folders are empty. Folder "TMP" stores code data files with check matrices, syndrome measurement circuits, and decoding matrices. There is a separate data file for each combination (code, error rate, number of syndrome cycles). Create code data files using decoder_setup.py. Folder "CODE_n_k_d" contains a file "result" that stores the simulation results. Each line in the "result" file has four columns: column 1: physical error rate, column 2: number of syndrome cycles, column 3: number of Monte Carlo trials, column 4: number of failed trials that resulted in a logical error. Each trial runs the noisy error correction circuit followed by a noiseless syndrome measurement of all stabilizers, decoding, and error correction. A trial is failed if error correction results in a non-identity logical Pauli error.

distance_test.py calculates the code distance by solving an integer linear program

run `python set_decoder_288.py` and `python set_decoder_170.py` to setup the decoder test for the [[288, 12, 22]] code and [[170, 16, 10]] code. Then run 
```
python decoder_run.py n k d [error_rate] [iterations]
``` 
to simulate the error of the [[n, k, d]] code. For example `python decoder_run.py 288 12 22 0.0035 10000` will simulate the logical error rate of the [[288, 12, 22]] code with base error 0.0035 for 10000 iterations. `python decoder_run.py 170 16 10 0.003 20000` will simulate the logical error rate of the [[170, 16, 10]] code with base error 0.0035 for 20000 iterations.

## Quantum Lego Codes Evaluation

We store the check matrix of all codes we list in the Table 2 under different noise model in the folder `QLegoCodes/foundBest`. To reproduce the result in Table 2, run the command below

```
cd QLegoCodes
python benchEval.py
```

## Utilize Funsearch to Search

This repo uses a fork version of Funsearch. The original version is from this [repo](https://github.com/google-deepmind/funsearch) which accompanies the publication 

Romera-Paredes, B. et al. [Mathematical discoveries from program search with large language models](https://www.nature.com/articles/s41586-023-06924-6). *Nature* (2023)

An example is shown in `BBcodeSearch/main.py` for how to configure Funsearch for searching heuristic functions in the Bivariate Bicycle code search. 

```python
with open("skeleton.py", "r") as f:
    content = f.read()
    sandbox = Sandbox(score)
    databaseConf = ProgramsDatabaseConfig(num_islands=1)
    conf = Config(
        sandbox=sandbox,
        programs_database=databaseConf,
        init_template="init_template/",
        prompt_manipulate=prompt_manipulate,
        num_samplers=1,
        num_evaluators=1,
        samples_per_prompt=1,
        iterations=5,
    )
    inputs = [None]
    main(content, inputs, conf)
```
The `main` function of Funsearch recieves three inputs. `content` is the skeleton of the program that needs to be evolve. The function to be evolved should be decorated with `@funsearch.evolve`. `conf` is the configuration sent to Funsearch. The class Config should be configured withh

- sandbox : define how to evaluate each candidate function evolved by Funsearch. It should return the score of the candidate function and a boolean variable representing whether the execution is successful.
- ProgramsDatabaseConfig: configuring the database (e.g. number of islands)
- prompt_manipulate: define how to manipulate the prompt before sending it to the LLM. The input to the function `prompt_manipulate` are two functions sampled from the database.
- iterations: Funsearch will terminate after reaching the iterations number.
  
optional

- init_template: initial possible implementation of the function to be evolved. Will be evaluated and inserted into the database at the starting point.