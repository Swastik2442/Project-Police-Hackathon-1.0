# Police Feedback System by Binary Brigade
This is our Project for the Problem Statement of **Police Feedback System**. The aim of this project is to cater the Feedback requirements of the Police while being advanced enough to support everyone in the society.

> Check more about the Problem Statement at https://www.police.rajasthan.gov.in/old/hackathon/.

### Setup
```bash
git clone https://github.com/Swastik2442/RJPOLICE_HACK_157_Binary_Brigade_1
cd RJPOLICE_HACK_157_Binary_Brigade_1
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
cp .envexample .env
nano .env # Edit with your Values
cd feedbackSystem
nano feedbackSystem/settings.py # Edit with your Values
python3 manage.py migrate
python3 manage.py compilemessages
python3 manage.py collectstatic
python3 manage.py runserver
```

<details>
  <summary>Deployment Setup</summary>

  ```bash
  sudo apt update
  sudo apt upgrade
  sudo apt install python3 python3-venv apache2 libapache2-mod-wsgi-py3

  # Proceed with the aforementioned Steps here and edit the values in settings.py

  sudo a2enmod wsgi
  sudo service restart apache2
  sudo chmod 755 /home/yourusername # Path for the Project
  sudo nano /etc/apache2/sites-available/000-default.conf # Edit with your Values
  sudo tail -f /var/log/apache2/error.log
  ```

</details>

### Uses
* [Django](https://www.djangoproject.com/)
* [Twilio](https://www.twilio.com/)
* [Bootstrap](https://getbootstrap.com/)
* [jQuery](https://jquery.com/)
* [Waypoints](http://imakewebthings.com/waypoints/)
* [Others](https://github.com/Swastik2442/RJPOLICE_HACK_157_Binary_Brigade_1/network/dependencies)

### Team Members
<a href="https://github.com/Swastik2442/RJPOLICE_HACK_157_Binary_Brigade_1/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Swastik2442/RJPOLICE_HACK_157_Binary_Brigade_1" />
</a>