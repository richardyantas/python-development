# createdb flashback
# dropdb flashback
# conda env create -f environment.yml
# conda env list
# chmod +x setup.sh
# conda init bash
# source  /home/serendipita/anaconda3/etc/profile.d/conda.sh

# does not works ! 

if [ $1 = "install" ]; then
  echo "Installing ... "
  createdb flashback
  conda env create -f environment.yml
elif [ $1 = "run" ]; then  
  echo "Running ... "
  eval "$(conda shell.bash hook)"
  conda activate lab2
elif [ $1 = "tests" ]; then
  echo "Testing ... "
fi
