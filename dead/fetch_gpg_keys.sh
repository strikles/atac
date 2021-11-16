#CSV of email address
csv=$1

# Get headers from CSV
headers=$(head -1 $csv)

# Find the column number of the email address
emailCol=$(echo $headers | tr ',' '\n' | grep -n "email" | cut -d':' -f1)

# Content of the CSV at emailCol column, skipping the first line
emailAddrs=$(tail -n +2 $csv | cut -d',' -f$emailCol)
gpgListPatrn='(?<entropy>\d+)\s*bit\s*(?<algo>\S+)\s*key\s*(?<pubkeyid>[^,]+)'
# Loop through the array and get the public keys
for email in "${emailAddrs[@]}"
do
    echo "${email}\n"
    # Get the public key ids for the email address by matching the regex gpgListPatt
    pubkeyids=$(gpg --batch --search-keys $email 2>&1 | grep -Po $gpgListPatrn | cut -d' ' -f5)
    # For each public key id, get the public key
    for pubkeyid in $pubkeyids
    do
        # Add the public key to the local keyring
        recvr=$(gpg --recv-keys $pubkeyids 2>&1)
        # Check exit code to see if the key was added
        if [ $? -eq 0 ]; then
            # If the public key is added, do some extra work with it
            echo "gpg key added to keyring\n"
        fi
    done
done
