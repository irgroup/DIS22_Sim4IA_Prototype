# Prototype Container for Sim4IA and DIS22

This prototype is build upon the implementation of the ![SimIIR3 Framework](https://github.com/simint-ai/simiir-3). To facilitate experimentation with this setup, please follow the installation guide below. For easy installation, a Docker setup is used.

## Installation

1. Open a terminal and navigate to the repository directory
2. Download the Index from Sciebo and unzip the index into `example_data/index_CORE.zip` file into the `example_data/index_CORE directory.
```shell
curl -L -o index_CORE.zip "https://th-koeln.sciebo.de/s/F9AEa1CXyk2RTpf/download"
unzip index_CORE.zip -d ./example_data/
``
3. Build the container by executing:
```shell

docker-compose up -d --build

```
If the container has already been built, you can start it with:
```shell

docker-compose up -d

```
4. All dependencies should be installed automatically
5. You can access the Docker container via your IDE (e.g., VS Code)

You can access the Docker container via your IDE (e.g., VS Code).
```shell

docker-compose down

```

##  How to do the experiments?

1. Adjust your query reformulation approach 
    - You can find existing implementations in `simiir/user/query_generators/`
2. Create a new user configuration that uses your query reformulation approach
    - Existing user configurations can be found in `example_sims/users/`
3. Add your new user configuration to the experimental setup
    - The setup is located in `example_sims/users/core_bm25_DIS22_Sim4IA.xml`    
4. Navigate to the `simiir` directory in the terminal
5. Run the configuration file with:
```shell

python run_simiir.py ../example_sims/core_bm25_DIS22_Sim4IA.xml 

```
6. Evaluate the results using the provided notebook
    - The evaluation notebook is located in `evaluation/eval_core.ipynb`

## License

This project is licensed under the MIT License - see the LICENSE file for details.



