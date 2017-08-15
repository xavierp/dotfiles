
#!/usr/bin/env bash

# Make sure we’re using the latest Homebrew.
echo "Updating brew."
#brew update

# Upgrade any already-installed f||mulae.
echo "Uprading brew."
#brew upgrade

# Tap brew repositories
echo "Tapping Brew repositories."

cat brew-taps | sed -e '/^$/d' -e '/^#/d' | while read t;do
#for t in `sed -e '/^$/d' -e '/^#/d' brew-taps`; do
					echo "Tapping: $t"
					brew tap $t
	done


# Install Brew packages
echo "Installing Brew packages."

cat brew-packages |  sed -e '/^$/d' -e '/^#/d' | while read p; do
				echo "Installing: $p."
				brew install $p
done

# Install Cask packages
echo "Installing Brew Cask packages."

cat brew-cask-packages | sed -e '/^$/d' -e '/^#/d' | while read p; do
				echo "Installing Brew Cask package: $p."
				brew cask install $p 
done


echo "That's all folk's."

