# Bootstrap for new computer

# Install `command_line_tools`
echo "Checking command-line-tools."
pkgutil --pkg-info=com.apple.pkg.CLTools_Executables > /dev/null 2> /dev/null
if [ "$?" -ne 0 ]
then
    echo "command-line-tools needs to be installed."
    echo "Lauching command_line_tools install."
    xcode-select --install > /dev/null 2> /dev/null

 else
 	echo "command_line_tools OK."
fi

# Wait for command_line_tools to be installed.
commandline=0
cutoff=100
while : ; do
	pkgutil --pkg-info=com.apple.pkg.CLTools_Executables > /dev/null 2> /dev/null
	retour=$?
	if [ "$retour" -eq 0 ]
	then
	   echo "command-line-tools: installed."
	   commandLine=1
	   break
	fi
	if [ "$cutoff" -lt 1 ]
	then
		echo "command_line_tools not found. Please install command_line_tools and start again."
            exit 1
	fi
	cutoff=$((cutoff-1))
	sleep 10
done


# Install Homebrew
echo "Checking Homebrew."

if [ `command -v brew` -ne 0]
then
		echo "Installing Homebrew"
		/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
	echo "Homebrew OK."
fi

# Copy .files to ~/
cp ./dotfiles/ ~/
