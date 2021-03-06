# devLab-3 pre-release

Advanced Machine-Learning Algorithms and Reinforcement Learning. (WIP)

This is the "Testing Grounds" for integrating with higher level DSL's, Modular Deep Reinforcement Learning, Smart-Contracts, RaspberryPi, and M-L algorithm Libraries/Notebooks.

# SLM Lab <br> ![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/kengz/slm-lab) ![CI](https://github.com/kengz/SLM-Lab/workflows/CI/badge.svg) [![Maintainability](https://api.codeclimate.com/v1/badges/20c6a124c468b4d3e967/maintainability)](https://codeclimate.com/github/kengz/SLM-Lab/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/20c6a124c468b4d3e967/test_coverage)](https://codeclimate.com/github/kengz/SLM-Lab/test_coverage)

<p align="center">
  <img src="demo.gif" alt="demo" />
</p>



<p align="center">
  <i>Modular Deep Reinforcement Learning framework in PyTorch.</i>
  <br><br>
  <b>Documentation:</b><br>
  <a href="https://slm-lab.gitbook.io/slm-lab/">https://slm-lab.gitbook.io/slm-lab/</a>
  <br><br>
</p>


|||||
|:---:|:---:|:---:|:---:|
| ![ppo beamrider](https://user-images.githubusercontent.com/8209263/63994698-689ecf00-caaa-11e9-991f-0a5e9c2f5804.gif) | ![ppo breakout](https://user-images.githubusercontent.com/8209263/63994695-650b4800-caaa-11e9-9982-2462738caa45.gif) | ![ppo kungfumaster](https://user-images.githubusercontent.com/8209263/63994690-60469400-caaa-11e9-9093-b1cd38cee5ae.gif) | ![ppo mspacman](https://user-images.githubusercontent.com/8209263/63994685-5cb30d00-caaa-11e9-8f35-78e29a7d60f5.gif) |
| BeamRider | Breakout | KungFuMaster | MsPacman |
| ![ppo pong](https://user-images.githubusercontent.com/8209263/63994680-59b81c80-caaa-11e9-9253-ed98370351cd.gif) | ![ppo qbert](https://user-images.githubusercontent.com/8209263/63994672-54f36880-caaa-11e9-9757-7780725b53af.gif) | ![ppo seaquest](https://user-images.githubusercontent.com/8209263/63994665-4dcc5a80-caaa-11e9-80bf-c21db818115b.gif) | ![ppo spaceinvaders](https://user-images.githubusercontent.com/8209263/63994624-15c51780-caaa-11e9-9c9a-854d3ce9066d.gif) |
| Pong | Qbert | Seaquest | Sp.Invaders |
| ![sac ant](https://user-images.githubusercontent.com/8209263/63994867-ff6b8b80-caaa-11e9-971e-2fac1cddcbac.gif) | ![sac halfcheetah](https://user-images.githubusercontent.com/8209263/63994869-01354f00-caab-11e9-8e11-3893d2c2419d.gif) | ![sac hopper](https://user-images.githubusercontent.com/8209263/63994871-0397a900-caab-11e9-9566-4ca23c54b2d4.gif) | ![sac humanoid](https://user-images.githubusercontent.com/8209263/63994883-0befe400-caab-11e9-9bcc-c30c885aad73.gif) |
| Ant | HalfCheetah | Hopper | Humanoid |
| ![sac doublependulum](https://user-images.githubusercontent.com/8209263/63994879-07c3c680-caab-11e9-974c-06cdd25bfd68.gif) | ![sac pendulum](https://user-images.githubusercontent.com/8209263/63994880-085c5d00-caab-11e9-850d-049401540e3b.gif) | ![sac reacher](https://user-images.githubusercontent.com/8209263/63994881-098d8a00-caab-11e9-8e19-a3b32d601b10.gif) | ![sac walker](https://user-images.githubusercontent.com/8209263/63994882-0abeb700-caab-11e9-9e19-b59dc5c43393.gif) |
| Inv.DoublePendulum | InvertedPendulum | Reacher | Walker |

# Algorithm Visualizer

> Algorithm Visualizer is an interactive online platform that visualizes algorithms from code.

[![GitHub contributors](https://img.shields.io/github/contributors/algorithm-visualizer/algorithm-visualizer.svg?style=flat-square)](https://github.com/algorithm-visualizer/algorithm-visualizer/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/algorithm-visualizer/algorithm-visualizer.svg?style=flat-square)](https://github.com/algorithm-visualizer/algorithm-visualizer/blob/master/LICENSE)

Learning an algorithm gets much easier with visualizing it. Don't get what we mean? Check it out:

[**algorithm-visualizer.org**![Screenshot](https://raw.githubusercontent.com/algorithm-visualizer/algorithm-visualizer/master/branding/screenshot.png)](https://algorithm-visualizer.org/)

## Contributing

We have multiple repositories under the hood that comprise the website. Take a look at the contributing guidelines in the repository you want to contribute to.

- [**`algorithm-visualizer`**](https://github.com/algorithm-visualizer/algorithm-visualizer) is a web app written in React. It contains UI components and interprets commands into visualizations. Check out [the contributing guidelines](CONTRIBUTING.md).

- [**`server`**](https://github.com/algorithm-visualizer/server) serves the web app and provides APIs that it needs on the fly. (e.g., GitHub sign in, compiling/running code, etc.)

- [**`algorithms`**](https://github.com/algorithm-visualizer/algorithms) contains visualizations of algorithms shown on the side menu of the website.

- [**`tracers.*`**](https://github.com/search?q=topic%3Avisualization-library+org%3Aalgorithm-visualizer&type=Repositories) are visualization libraries written in each supported language. They extract visualizing commands from code.

NOTICE:
CODE_OF_CONDUCT 

Copyright ????? Justin Mitchell.  MitchellTesla~ 2021
 
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

Our Standards
Examples of behavior that contributes to creating a positive environment include:

Using welcoming and inclusive language
Being respectful of differing viewpoints and experiences
Gracefully accepting constructive criticism
Focusing on what is best for the community
Showing empathy towards other community members


Examples of unacceptable behavior by participants include:

The use of sexualized language or imagery and unwelcome sexual attention or advances
Trolling, insulting/derogatory comments, and personal or political attacks
Public or private harassment

Publishing others' private information, such as a physical or electronic address, without explicit permission
Other conduct which could reasonably be considered inappropriate in a professional setting

Our Responsibilities
Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

Scope
This Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project e-mail address, posting via an official social media account, or acting as an appointed representative at an online or offline event. Representation of a project may be further defined and clarified by project maintainers.

Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the projects Lead Developer at Mitchelltesla103@gmail.com . All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident. Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.



NOTICE:

MIT License

Copyright (c) 2021 Justin Mitchell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


NOTICE: LICENSE #2

Cryptographic Autonomy License version 1.0

This Cryptographic Autonomy License (the ???License???) applies to any Work whose owner has marked it with any of the following notices:

???Licensed under the Cryptographic Autonomy License version 1.0,??? or

???SPDX-License-Identifier: CAL-1.0,??? or

???Licensed under the Cryptographic Autonomy License version 1.0, with Combined Work Exception,??? or

???SPDX-License-Identifier: CAL-1.0 with Combined-Work-Exception.???

1. Purpose
This License gives You unlimited permission to use and modify the software to which it applies (the ???Work???), either as-is or in modified form, for Your private purposes, while protecting the owners and contributors to the software from liability.

This License also strives to protect the freedom and autonomy of third parties who receive the Work from you. If any non-affiliated third party receives any part, aspect, or element of the Work from You, this License requires that You provide that third party all the permissions and materials needed to independently use and modify the Work without that third party having a loss of data or capability due to your actions.

The full permissions, conditions, and other terms are laid out below.

2. Receiving a License
In order to receive this License, You must agree to its rules. The rules of this License are both obligations of Your agreement with the Licensor and conditions to your License. You must not do anything with the Work that triggers a rule You cannot or will not follow.

2.1. Application
The terms of this License apply to the Work as you receive it from Licensor, as well as to any modifications, elaborations, or implementations created by You that contain any licenseable portion of the Work (a ???Modified Work???). Unless specified, any reference to the Work also applies to a Modified Work.

2.2. Offer and Acceptance
This License is automatically offered to every person and organization. You show that you accept this License and agree to its conditions by taking any action with the Work that, absent this License, would infringe any intellectual property right held by Licensor.

2.3. Compliance and Remedies
Any failure to act according to the terms and conditions of this License places Your use of the Work outside the scope of the License and infringes the intellectual property rights of the Licensor. In the event of infringement, the terms and conditions of this License may be enforced by Licensor under the intellectual property laws of any jurisdiction to which You are subject. You also agree that either the Licensor or a Recipient (as an intended third-party beneficiary) may enforce the terms and conditions of this License against You via specific performance.

3. Permissions and Conditions
3.1. Permissions Granted
Conditioned on compliance with section 4, and subject to the limitations of section 3.2, Licensor grants You the world-wide, royalty-free, non-exclusive permission to:

a) Take any action with the Work that would infringe the non-patent intellectual property laws of any jurisdiction to which You are subject; and

b) Take any action with the Work that would infringe any patent claims that Licensor can license or becomes able to license, to the extent that those claims are embodied in the Work as distributed by Licensor.

3.2. Limitations on Permissions Granted
The following limitations apply to the permissions granted in section 3.1:

a) Licensor does not grant any patent license for claims that are only infringed due to modification of the Work as provided by Licensor, or the combination of the Work as provided by Licensor, directly or indirectly, with any other component, including other software or hardware.

b) Licensor does not grant any license to the trademarks, service marks, or logos of Licensor, except to the extent necessary to comply with the attribution conditions in section 4.1 of this License.

4. Conditions
If You exercise any permission granted by this License, such that the Work, or any part, aspect, or element of the Work, is distributed, communicated, made available, or made perceptible to a non-Affiliate third party (a ???Recipient???), either via physical delivery or via a network connection to the Recipient, You must comply with the following conditions:

4.1. Provide Access to Source Code
Subject to the exception in section 4.4, You must provide to each Recipient a copy of, or no-charge unrestricted network access to, the Source Code corresponding to the Work.

The ???Source Code??? of the Work means the form of the Work preferred for making modifications, including any comments, configuration information, documentation, help materials, installation instructions, cryptographic seeds or keys, and any information reasonably necessary for the Recipient to independently compile and use the Source Code and to have full access to the functionality contained in the Work.

4.1.1. Providing Network Access to the Source Code
Network access to the Notices and Source Code may be provided by You or by a third party, such as a public software repository, and must persist during the same period in which You exercise any of the permissions granted to You under this License and for at least one year thereafter.

4.1.2. Source Code for a Modified Work
Subject to the exception in section 4.5, You must provide to each Recipient of a Modified Work Access to Source Code corresponding to those portions of the Work remaining in the Modified Work as well as the modifications used by You to create the Modified Work. The Source Code corresponding to the modifications in the Modified Work must be provided to the Recipient either a) under this License, or b) under a Compatible Open Source License.

A ???Compatible Open Source License??? means a license accepted by the Open Source Initiative that allows object code created using both Source Code provided under this License and Source Code provided under the other open source license to be distributed together as a single work.

4.1.3. Coordinated Disclosure of Security Vulnerabilities
You may delay providing the Source Code corresponding to a particular modification of the Work for up to ninety (90) days (the ???Embargo Period???) if: a) the modification is intended to address a newly-identified vulnerability or a security flaw in the Work, b) disclosure of the vulnerability or security flaw before the end of the Embargo Period would put the data, identity, or autonomy of one or more Recipients of the Work at significant risk, c) You are participating in a coordinated disclosure of the vulnerability or security flaw with one or more additional Licensees, and d) Access to the Source Code pertaining to the modification is provided to all Recipients at the end of the Embargo Period.

4.2. Maintain User Autonomy
In addition to providing each Recipient the opportunity to have Access to the Source Code, You cannot use the permissions given under this License to interfere with a Recipient???s ability to fully use an independent copy of the Work generated from the Source Code You provide with the Recipient???s own User Data.

???User Data??? means any data that is an input to or an output from the Work, where the presence of the data is necessary for substantially identical use of the Work in an equivalent context chosen by the Recipient, and where the Recipient has an existing ownership interest, an existing right to possess, or where the data has been generated by, for, or has been assigned to the Recipient.

4.2.1. No Withholding User Data
Throughout any period in which You exercise any of the permissions granted to You under this License, You must also provide to any Recipient to whom you provide services via the Work, a no-charge copy, provided in a commonly used electronic form, of the Recipient???s User Data in your possession, to the extent that such User Data is available to You for use in conjunction with the Work.

4.2.2. No Technical Measures that Limit Access
You may not, by the use of cryptographic methods applied to anything provided to the Recipient, by possession or control of cryptographic keys, seeds, or hashes, by other technological protection measures, or by any other method, limit a Recipient's ability to access any functionality present in the Recipient's independent copy of the Work, or deny a Recipient full control of the Recipient's User Data.

4.2.3. No Legal or Contractual Measures that Limit Access
You may not contractually restrict a Recipient's ability to independently exercise the permissions granted under this License. You waive any legal power to forbid circumvention of technical protection measures that include use of the Work, and You waive any claim that the capabilities of the Work were limited or modified as a means of enforcing the legal rights of third parties against Recipients.

4.3. Provide Notices and Attribution
You must retain all licensing, authorship, or attribution notices contained in the Source Code (the ???Notices???), and provide all such Notices to each Recipient, together with a statement acknowledging the use of the Work. Notices may be provided directly to a Recipient or via an easy-to-find hyperlink to an Internet location also providing Access to Source Code.

4.4. Scope of Conditions in this License
You are required to uphold the conditions of this License only relative to those who are Recipients of the Work from You. Other than providing Recipients with the applicable Notices, Access to Source Code, and a copy of and full control of their User Data, nothing in this License requires You to provide processing services to or engage in network interactions with anyone.

4.5. Combined Work Exception
As an exception to condition that You provide Recipients Access to Source Code, any Source Code files marked by the Licensor as having the ???Combined Work Exception,??? or any object code exclusively resulting from Source Code files so marked, may be combined with other Software into a ???Larger Work.??? So long as you comply with the requirements to provide Recipients the applicable Notices and Access to the Source Code provided to You by Licensor, and you provide Recipients access to their User Data and do not limit Recipient???s ability to independently work with their User Data, any other Software in the Larger Work as well as the Larger Work as a whole may be licensed under the terms of your choice.

5. Term and Termination
The term of this License begins when You receive the Work, and continues until terminated for any of the reasons described herein, or until all Licensor???s intellectual property rights in the Software expire, whichever comes first (???Term???). This License cannot be revoked, only terminated for the reasons listed below.

5.1. Effect of Termination
If this License is terminated for any reason, all permissions granted to You under Section 3 by any Licensor automatically terminate. You will immediately cease exercising any permissions granted in this License relative to the Work, including as part of any Modified Work.

5.2. Termination for Non-Compliance; Reinstatement
This License terminates automatically if You fail to comply with any of the conditions in section 4. As a special exception to termination for non-compliance, Your permissions for the Work under this License will automatically be reinstated if You come into compliance with all the conditions in section 2 within sixty (60) days of being notified by Licensor or an intended third party beneficiary of Your noncompliance. You are eligible for reinstatement of permissions for the Work one time only, and only for the sixty days immediately after becoming aware of noncompliance. Loss of permissions granted for the Work under this License due to either a) sustained noncompliance lasting more than sixty days or b) subsequent termination for noncompliance after reinstatement, is permanent, unless rights are specifically restored by Licensor in writing.

5.3 Termination Due to Litigation
If You initiate litigation against Licensor, or any Recipient of the Work, either direct or indirect, asserting that the Work directly or indirectly infringes any patent, then all permissions granted to You by this License shall terminate. In the event of termination due to litigation, all permissions validly granted by You under this License, directly or indirectly, shall survive termination. Administrative review procedures, declaratory judgment actions, counterclaims in response to patent litigation, and enforcement actions against former Licensees terminated under this section do not cause termination due to litigation.

6. Disclaimer of Warranty and Limit on Liability
As far as the law allows, the Work comes AS-IS, without any warranty of any kind, and no Licensor or contributor will be liable to anyone for any damages related to this software or this license, under any kind of legal claim, or for any type of damages, including indirect, special, incidental, or consequential damages of any type arising as a result of this License or the use of the Work including, without limitation, damages for loss of goodwill, work stoppage, computer failure or malfunction, loss of profits, revenue, or any and all other commercial damages or losses.

7. Other Provisions
7.1. Affiliates
An ???Affiliate??? means any other entity that, directly or indirectly through one or more intermediaries, controls, is controlled by, or is under common control with, the Licensee. Employees of a Licensee and natural persons acting as contractors exclusively providing services to Licensee are also Affiliates.

7.2. Choice of Jurisdiction and Governing Law
A Licensor may require that any action or suit by a Licensee relating to a Work provided by Licensor under this License may be brought only in the courts of a particular jurisdiction and under the laws of a particular jurisdiction (excluding its conflict-of-law provisions), if Licensor provides conspicuous notice of the particular jurisdiction to all Licensees.

7.3. No Sublicensing
This License is not sublicensable. Each time You provide the Work or a Modified Work to a Recipient, the Recipient automatically receives a license under the terms described in this License. You may not impose any further reservations, conditions, or other provisions on any Recipients??? exercise of the permissions granted herein.

7.4. Attorneys' Fees
In any action to enforce the terms of this License, or seeking damages relating thereto, including by an intended third party beneficiary, the prevailing party shall be entitled to recover its costs and expenses, including, without limitation, reasonable attorneys' fees and costs incurred in connection with such action, including any appeal of such action. A ???prevailing party??? is the party that achieves, or avoids, compliance with this License, including through settlement. This section shall survive the termination of this License.

7.5. No Waiver
Any failure by Licensor to enforce any provision of this License will not constitute a present or future waiver of such provision nor limit Licensor???s ability to enforce such provision at a later time.

7.6. Severability
If any provision of this License is held to be unenforceable, such provision shall be reformed only to the extent necessary to make it enforceable. Any invalid or unenforceable portion will be interpreted to the effect and intent of the original portion. If such a construction is not possible, the invalid or unenforceable portion will be severed from this License but the rest of this License will remain in full force and effect.

7.7. License for the Text of this License
The text of this license is released under the Creative Commons Attribution-ShareAlike 4.0 International License, with the caveat that any modifications of this license may not use the name ???Cryptographic Autonomy License??? or any name confusingly similar thereto to describe any derived work of this License.



Copyright (c)  Justin Mitchell  2021  MIT LICENSE

