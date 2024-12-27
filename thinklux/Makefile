all: build install install_sudoers
build:
	g++ thinkled.cpp
install:
	sudo cp a.out /usr/local/sbin/thinkled
	sudo cp thinkled.timer thinkled.service /etc/systemd/system/
	sudo systemctl enable thinkled.timer thinkled.service
install_sudoers:
	echo "$(shell whoami) ALL=(root) NOPASSWD: sha256:$(shell sha256sum /usr/local/sbin/thinkled)" | sudo tee /etc/sudoers.d/thinkled
clean:
	sudo systemctl disable thinkled.timer thinkled.service
	sudo rm /etc/systemd/system/thinkled.timer /etc/systemd/system/thinkled.service /usr/local/sbin/thinkled /etc/sudoers.d/thinkled
	rm a.out
