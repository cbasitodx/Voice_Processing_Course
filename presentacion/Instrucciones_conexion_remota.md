PASOS: 

1. Crear red en Hamachi: 


        sudo hamachi create DSPRed DSPRed123

2. Conectarse a la red de Hamachi (comprobar con un ping):

        sudo hamachi join [nombre_de_red] [contraseña]

3. Obtener IP de Hamachi con ```ifconfig``` (ham0)

4. Abrir VLC: 

        vlc --rc-host [IP HAMACHI]:54321 senal_audio_directa.wav & vlc --rc-host [IP HAMACHI]:12345 senal_audio_directa.wav
        
5. Lanzar VLSync: 

        vlcsync --rc-host [IP HAMACHI]:54321 --rc-host [IP HAMACHI]:12345 --volume-sync