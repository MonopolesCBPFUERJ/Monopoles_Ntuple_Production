#!/bin/bash

# Carregar o ambiente CMSSW
source /cvmfs/cms.cern.ch/cmsset_default.sh

# Definir o caminho da proxy para acesso aos dados
export X509_USER_PROXY=/afs/cern.ch/user/t/tmenezes/work/public/x509up_u81013


# Navegar para o diretório do CMSSW
cd /afs/cern.ch/user/t/tmenezes/work/public/CMSSW_10_6_23/src
eval `scramv1 runtime -sh`

# Argumento passado pelo Condor (o caminho do arquivo de entrada)
input_file=$1
#input_file='/store/mc/RunIISummer20UL18RECO/Monopole_SpinHalf_DrellYan_M-1500_TuneCP5_13TeV_madgraph-pythia8/GEN-SIM-RECO/106X_upgrade2018_realistic_v11_L1v1-v2/130000/71F3498E-24AB-A34F-BB44-B8CA72614E4B.root'

# Variável para definir o ano diretamente no script
year=2018  # Modifique este valor conforme necessário (2016, 2016APV, 2017)

# Caminhos dos arquivos de configuração
config_2016APV="ntuple_mc_2016APV_cfg.py"
config_2016="ntuple_mc_2016_cfg.py"
config_2017="ntuple_mc_2017_cfg.py"
#config_2018="ntuple_mc_2018_cfg.py"
config_2018="ntuple_mc_2018_cfg_METFilter.py"

# Diretório de saída
#output_dir="/eos/user/t/tmenezes/Monopole_Ntuples/Central_Production/2018/"

output_dir="/eos/user/t/tmenezes/Monopole_Ntuples/Central_Production/15Jan_L1MET/2018/"

# Certifique-se de que o diretório de saída existe
mkdir -p $output_dir

# Extrair o nome do processo e o identificador único do nome do arquivo
process_name=$(echo $input_file | grep -oP 'Monopole_[A-Za-z]+_[A-Za-z]+_M-\d+')
file_id=$(basename $input_file .root)  # Nome do arquivo sem extensão

# Verificar se os campos foram extraídos corretamente
if [ -z "$process_name" ]; then
    echo "Erro: Não foi possível extrair o nome do processo do arquivo $input_file"
    exit 1
fi

if [ -z "$file_id" ]; then
    echo "Erro: Não foi possível extrair o identificador único do arquivo $input_file"
    exit 1
fi

# Nome de saída no formato esperado
output_file="${process_name}_${year}_${file_id}.root"

# Função para executar o cmsRun
run_cms() {
    local config_file=$1
    local input_file=$2
    local output_file=$3
    echo "Running: cmsRun $config_file inputFiles=$input_file outputFile=$output_file"
    cmsRun $config_file inputFiles=$input_file outputFile=$output_file
    echo "Job for year $year, file $input_file, and process $process_name completed."
}

# Executar de acordo com o ano especificado
if [ "$year" == "2016APV" ]; then
    run_cms $config_2016APV "file:root://cms-xrd-global.cern.ch//$input_file" "$output_dir/$output_file"
elif [ "$year" == "2016" ]; then
    run_cms $config_2016 "file:root://cms-xrd-global.cern.ch//$input_file" "$output_dir/$output_file"
elif [ "$year" == "2017" ]; then
    run_cms $config_2017 "file:root://cms-xrd-global.cern.ch//$input_file" "$output_dir/$output_file"
elif [ "$year" == "2018" ]; then
    #run_cms $config_2018 "file:$input_file" "$output_dir/$output_file"
    run_cms $config_2018 "file:root://cms-xrd-global.cern.ch//$input_file" "$output_dir/$output_file"
else
    echo "Ano inválido. Por favor, especifique 2016, 2016APV, 2017 ou 2018."
    exit 1
fi
