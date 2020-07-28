- Install awsCLI and boto3:
    - pip install boto3 --user (or pip3 install boto3 --user)
    - Mac client available at: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html 
    - Run the `$ aws configure` setup
    - Set access key, secret key, region and output format

- Instead of passing the credentials in the script, it is recommanded to install awscli and setup credential profile. If running as a microservice, simply hit the endpoint in the script instead.

- If running on a computer, keep the Input file and script in the same dir to avoid search path failures.

- Run script `python3 <input-file-name with extension> <output-file-name with extension>
    - E.g `python3 lightweighttranscribe.py sample3.wav converted.txt`

- Output file will be created in same dir as script in case you don't specify path.
