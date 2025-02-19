## February 2025: MASSIVE UPDATES COMING INCLUDING FULLY COMPILED EXE INSTALL THIS PROJECT HAS NOT BEEN ABANDONED IVE JUST BEEN REALLY BUSY!
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL-3.0 License][license-shield]][license-url]
[![YouTube][youtube-shield]][youtube-url]
[![Discord][discord-shield]][discord-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/DogeLord081/OneReality">
    <img src="OneReality Logo Transparent.png" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">OneReality</h3>

  <p align="center">
    Redefining Reality
    <br />
    <br />
    <a href="https://youtu.be/ieWZZzAFjsA">Demo video with 3D printed hologram box</a>
    ·
    <a href="https://github.com/DogeLord081/OneReality/issues">Report Bug</a>
    ·
    <a href="https://github.com/DogeLord081/OneReality/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

## !Please don't attempt to install this right now, the project is undergoing major changes and exllamav2 likely will throw many errors!

[![Demo](https://github.com/DogeLord081/OneReality-README/blob/master/Thumbnail.png)](https://youtu.be/ieWZZzAFjsA)
Click on image for demo video

A virtual waifu / assistant that you can speak to through your mic and it'll speak back to you! Has many features such as:

* Can be used in virtual reality, with a 3d hologram box, or on your computer
* You can speak to her with a mic
* It can speak back to you
* Has short-term memory and long-term memory
* Can open apps
* Smarter than you
* Fluent in  English, Japanese, Korean, and Chinese
* Can control your smart home like Alexa if you set up Tuya (more info in [Prerequisites](https://github.com/DogeLord081/OneReality#prerequisites))

More features I'm planning to add soon in the [Roadmap](https://github.com/DogeLord081/OneReality#roadmap). Also, here's a summary of how it works for those of you who want to know:

First, the Python package SpeechRecognition recognizes what you say into your mic, then that speech is written into an audio (.wav) file, which is sent to OpenAI's Whisper speech-to-text transcription AI, and the transcribed result is printed in the terminal and written in a conversation.jsonl which the vector database hyperdb uses cosine similarity on to find 2 of the closest matches to what you said in the conversation.jsonl and appends that to the prompt to give Megumin context, the response is then passed through multiple NLE RTE and other checks to see if you want to open an app or do something with your smarthome, the prompt is then sent to llama.cpp, and the response from Megumin is printed to the terminal and appended to conversation.jsonl, and finally, the response is spoken by VITS TTS.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org)
* [Llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
* [Whisper](https://openai.com/research/whisper)
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
* [PocketSphinx](https://pypi.org/project/pocketsphinx/)
* [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)
* [VITS-simple-api](https://github.com/Artrajz/vits-simple-api)
* [HyperDB](https://github.com/jdagdelen/hyperDB)
* [Sentence Transformers](https://github.com/UKPLab/sentence-transformers)
* [Tuya Cloud IoT](https://iot.tuya.com/)
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

1. [Install Python 3.10.11](https://www.python.org/downloads/release/python-31011/) and set it as an environment variable in PATH
2. [Install GIT](https://git-scm.com/downloads)
3. [Install CUDA 11.7 if you have an Nvidia GPU](https://developer.nvidia.com/cuda-11-7-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local)
4. [Install Visual Studio Community 2022](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030&passive=false) and select `Desktop Development with C++` in the install options
5. [Install VTube Studio on Steam](https://store.steampowered.com/app/1325860/VTube_Studio/)
6. [Download Megumin's VTube Studio Model](https://www.reddit.com/r/Megumin/comments/eibk52/i_ripped_the_megumin_model_from_the_isekai_app/)
7. Extract the downloaded zip so it's only one folder deep (you should be able to open the folder and have all the files there, not one folder containing everything)
8. Open VTube Studio > Settings icon > `Open Data Folder` and move the folder there > Person icon > c001_f_costume_kouma
9. [Install VB Cable Audio Driver](https://vb-audio.com/Cable/), but don't set it as your audio devices just yet
10. Open Control Panel > Sound and Hardware > Sound > Recording > find CABLE Output > right-click > Properties > Listen > Check `Listen to this device` > For `Playback through this device`, select your headphones or speakers
11. (Optional) Create a Tuya cloud project if you want to control your smart devices with the AI, for example, you can say 'Hey Megumin, can you turn on my LEDs' it's a bit complicated though and I'll probably make a video on it later because it's hard to explain through text, but here's a guide that should help you out: [https://developer.tuya.com/en/docs/iot/device-control-practice?id=Kat1jdeul4uf8](https://developer.tuya.com/en/docs/iot/device-control-practice?id=Kat1jdeul4uf8)


### Automatic Installation
1. Open cmd in whatever folder you want the project to be in, and run `git clone --recurse-submodules https://github.com/DogeLord081/OneReality.git`
2. Open the folder and run `python setup.py` and follow the instructions
3. Edit the variables in `.env` if you must
4. Run `OneReality.bat` and while it's running, open the start menu and type `Sound Mixer Options` and open it. You might have to wait and make Megumin say something first, but you should see Python in the App Volume list
5. Change the output to `CABLE Input (VB-Audio Virtual Cable)`
6. Open VTube Studio > Settings icon > Scroll to Microphone Settings > Select Microphone > CABLE Output (VB-Audio Virtual Cable) > Person with settings icon > Scroll to Mouth Smile > Copy [these settings](https://imgur.com/a/pf4SCSC) > Scroll to Mouth Open > Copy [these settings](https://imgur.com/a/dvWLloq)
7. Open `Sound Mixer Options` again and change the input for VTube Studio to `CABLE Output (VB-Audio Virtual Cable)`
8. May need to restart computer if lip sync doesn't work
9. You're good to go! If you run into any issues, let me know on Discord and I can help you. Once again, it's https://discord.gg/PN48PZEXJS
10. When you want to stop, say goodbye, bye, or see you somewhere in your sentence because that automatically ends the program, otherwise you can just ctrl + c or close the window
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Long-term memory
- [x] Time and date awareness
- [x] Virtual reality / augmented reality / mixed reality integration
- [x] Gatebox-style hologram
- [ ] Animatronic body
- [x] Alexa-like smart home control
- [x] More languages for the AI's voice
  - [x] Japanese
  - [x] English
  - [x] Korean
  - [x] Chinese
  - [ ] Spanish
  - [ ] Indonesian
- [ ] Mobile version
- [x] Easier setup
- [ ] Compiling into one exe
- [x] Localized
- [ ] VTube Studio lip-sync without driver like in [this project](https://github.com/AlizerUncaged/desktop-waifu) but I don't really understand the VTube Studio API used here

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact and Socials

E-mail: danu0518@gmail.com

YouTube: [https://www.be.com/@OneReality-tb4ut](https://www.be.com/@OneReality-tb4ut)

Discord: [https://discord.gg/PN48PZEXJS](https://discord.gg/PN48PZEXJS)

Project Link: [https://github.com/DogeLord081/OneReality](https://github.com/DogeLord081/OneReality)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments and Major Contributors

* [Choose an Open Source License](https://choosealicense.com)
* [AI Waifu Vtuber](https://github.com/ardha27/AI-Waifu-Vtuber)
* [SchizoDev](https://.be/dKFnJCtcfMk)
* xor
* jaxfry

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[discord-shield]: https://img.shields.io/discord/1123252189708693516?style=for-the-badge&label=DISCORD&color=%237289da
[discord-url]: https://discord.gg/eMnbhjW3GB
[youtube-shield]: https://img.shields.io/youtube/channel/subscribers/UC03Puq3SCjGWDPAnYGXjqQg?style=for-the-badge
[youtube-url]: https://www.youtube.com/@OneReality-tb4ut
[contributors-shield]: https://img.shields.io/github/contributors/DogeLord081/OneReality.svg?style=for-the-badge
[contributors-url]: https://github.com/DogeLord081/OneReality/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DogeLord081/OneReality.svg?style=for-the-badge
[forks-url]: https://github.com/DogeLord081/OneReality/network/members
[stars-shield]: https://img.shields.io/github/stars/DogeLord081/OneReality.svg?style=for-the-badge
[stars-url]: https://github.com/DogeLord081/OneReality/stargazers
[issues-shield]: https://img.shields.io/github/issues/DogeLord081/OneReality.svg?style=for-the-badge
[issues-url]: https://github.com/DogeLord081/OneReality/issues
[license-shield]: https://img.shields.io/github/license/DogeLord081/OneReality.svg?style=for-the-badge
[license-url]: https://github.com/DogeLord081/OneReality/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
