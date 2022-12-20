# Trabalho 1 de FSE

## Para rodar o projeto
- É necessário escolher uma placa como servidor central e outras N placas como servidores distruídos.
- Após isso basta adcionar a pasta referente a decisão nas placas.

### Execução Servidor Central
- Para executar o servidor central basta adicionar o ip do servidor escolhido e a porta no arquivo main.py e rodar o comando:

``` pyhton3 main.py ```

### Execução Servidor Distribuído
- Para executar o servidor distribído basta adaptar um dos arquivos json presentes na pasta configs com o Ip e porta da placa em que servirá como servidor central e a placa que será utilizada como servidor distribuído. Após isso basta rodar o comando:

``` python3 main.py [nomeArquivoJson] ``` 
