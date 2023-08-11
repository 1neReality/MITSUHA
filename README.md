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
    Bridging the real and virtual worlds
    <br />
    <br />
    <a href="https://youtu.be/eZridsHbooE">Demo Video (Lipsynced to Megumin in VTube Studio)</a>
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

[![Demo](https://github.com/DogeLord081/OneReality-README/blob/master/image.png)](https://youtu.be/eZridsHbooE)
Click on image for demo video

A virtual waifu / assistant that you can speak to through your mic and it'll speak back to you! Has many features such as:

* You can speak to her with a mic
* It can speak back to you in Japanese or English
* Has short-term memory (can remember things from the current conversation. Multi-conversation memory would take too long to respond and cost too much on the OpenAI API)
* Can open apps as long as you specify the app path in the code
* Knows everything ChatGPT does since they use pretty much the same models (ChatGPT uses the GPT-3.5-Turbo model while this uses the text-davinci-003 model)

More features I'm planning to add soon in the [roadmap](https://github.com/DogeLord081/OneReality#roadmap). Also, here's a summary of how it works for those of you who want to know:

First, the Python package SpeechRecognition recognizes what you say into your mic, then that speech is written into an audio (.wav) file, which is sent to OpenAI's Whisper speech to text transcription AI, and the transcribed result is printed in the terminal and sent to OpenAI's GPT-3, then GPT's response will be printed in the terminal and sent to PiperTTS which will generate and play an audio file with Megumin's voice reading the text (In English). All of this happens anywhere between 2-10 seconds, depending on the length of what you say, the length of what the AI says, and your GPU or CPU.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org)
* [GPT](https://openai.com/gpt-4)
* [Whisper](https://openai.com/research/whisper)
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
* [PocketSphinx](https://pypi.org/project/pocketsphinx/)
* [Google Translate](https://translate.google.com)
* [VoiceVox](https://voicevox.hiroshiba.jp)
* [PiperTTS](https://github.com/rhasspy/piper)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

[Video tutorial](https://youtu.be/qWpYE447iQA) (outdated don't watch this one). Here's how you can set it up on Windows (probably similar steps on Mac and Linux but I haven't tested them).

### Prerequisites

1. [Purchase an OpenAI API key](https://www.windowscentral.com/software-apps/how-to-get-an-openai-api-key). It's extremely affordable, since it's pay as you go, and I've been using it for a couple minutes a day like 3 times a week and I got charged less than a dollar for this month.
2. [Install Python](https://www.python.org/downloads/) and set it as an environment variable in PATH
3. [Download the source code](https://github.com/DogeLord081/OneReality/archive/refs/heads/main.zip)
4. Install WSL2 by opening a cmd in admin and running `wsl --install`
5. Set default distro version to WSL2 with `wsl --set-default-version 2`
6. Install [Ubuntu 22.04.2 WSL2 from Microsoft Store](https://apps.microsoft.com/store/detail/ubuntu-22042-lts/9PN20MSR04DW?hl=en-us&gl=us&rtc=1)

### Installation

1. Check that Ubuntu is WSL2 and not WSL1 by running `wsl -l -v` in cmd. If it says 1, run `wsl --set-version Ubuntu-22.04 2`
2. In the start menu, find the app `Ubuntu 22.04.2 LTS` and open it
3. In the terminal that pops up, run `git clone https://github.com/rhasspy/piper.git`
4. Extract the `OneReality-main` folder from prerequisites step 3 so that it is only one folder deep and rename the folder to just `OneReality`
5. Install the Python dependencies with pip by cding into the folder and running `pip install -r requirements.txt` in cmd or powershell
6. Add an empty text file in the OneReality-main folder called `conversation.txt`
7. Download `model.onnx` and `model.onnx.json` from [Huggingface](https://huggingface.co/DogeLord/megumin/tree/main) and make a folder called `model` in the `OneReality` folder and put the two files in it
8. Edit the code in `OneRealityENPublic.py` according to the comments within the code (you don't have to do anything complicated, just edit some filepaths and the OpenAI API key. Don't forget lines 154 and 185, they are the file paths to the model and output wav. /mnt/c/... means C:\... but you have to keep it as /mnt/c/... not C:\... because then WSL2 can't access it. So if the path to your model is `C:\Users\danu0\Downloads\OneReality\model9\model.onnx`, you'd make it `/mnt/c/Users/danu0/Downloads/OneReality/model9/model.onnx`)
9. Run `OneReality.bat` and you're good to go! If you run into any issues, let me know on Discord and I might be able to help you. Once again, it's https://discord.gg/PN48PZEXJS
10. When you want to stop, say goodbye, bye, or see you somewhere in your sentence because that automatically clears the `conversation.txt`. If you don't, it's fine you can just manually delete everything in the file

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Long-term memory
- [ ] Virtual reality / augmented reality / mixed reality integration
- [ ] Making an Alexa type of thing with it, or possibly a hologram like Gatebox?
- [ ] More languages for the AI's voice
  - [x] Japanese
  - [x] English
  - [ ] Korean
  - [ ] Chinese
  - [ ] Spanish
  - [ ] Indonesian
- [ ] Mobile version
- [ ] Easier setup
- [ ] Compiling into one exe

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact and Socials

E-mail: danu0518@gmail.com

YouTube: [https://www.youtube.com/@OneReality-tb4ut](https://www.youtube.com/@OneReality-tb4ut)

Discord: [https://discord.gg/PN48PZEXJS](https://discord.gg/PN48PZEXJS)

Project Link: [https://github.com/DogeLord081/OneReality](https://github.com/DogeLord081/OneReality)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [AI Waifu Vtuber](https://github.com/ardha27/AI-Waifu-Vtuber)
* [SchizoDev](https://youtu.be/dKFnJCtcfMk)

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
