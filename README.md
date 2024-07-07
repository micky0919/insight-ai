# Insight AI  
- Transforming natural language into structured data and stunning BI visualizations.

- Unlock insights from data effortlessly, streamlining analysis workflow and empowering data-driven decision making.

- Experience the future of data exploration today with innovative GenAI tool.


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

https://github.com/micky0919/insight-ai/assets/79015802/922f4fe2-2410-4046-9cf8-0c62e6c3a51a

Insight AI is a powerful analysis tool that leverage Large Language Models (LLMs) to generate datasets, visualizations, and dashboards based on user prompts. By providing guidance, users can obtain insightful responses from the model.

The core capabilities of Insight AI encompass the following aspects:

**RAG (Retrieval Augmented Generation)**: RAG is a highly sought-after and extensively implemented domain. Within the Insight AI framework, a comprehensive RAG-based framework for text-to-SQL has been developed, allowing users to leverage the RAG capabilities of LLMs.

**GBI (Generative Business Intelligence)**: GBI plays a fundamental role in the Insight AI project, offering indispensable data intelligence technology for constructing enterprise report analysis and generating business insights.

**Seamless Integration with Dashboard Tools**: Direct import of query results into a dashboard builder enables intuitive data exploration. Moreover, BI Wizard facilitates the generation of various visualizations based on user prompts.

**Fine-tuning Framework**: Insight AI provides a comprehensive fine-tuning framework for improving the accuracy of the result from LLM, incorporating features such as RAG (Retrieval Augmented Generation), Dynamic Few-Shot Prompt Strategy, and Multi-Agent Validation.

**Multi-Agents Framework**: The Multi-Agents Framework within Insight AI is a data-driven and self-evolving system consisting of multiple LLM agents, each responsible for different areas of insight discovery. These agents work collaboratively to validate the generated results and make necessary self-corrections based on ongoing analysis and feedback.

To experience Insight AI yourself, please feel free to access the application on [Streamlit Cloud](https://insightai.streamlit.app/
). 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

### Installation

1. Get a OpenAI API Key
2. Clone the repo
   ```sh
   git clone https://github.com/micky0919/insight-ai.git
   ```
3. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```
4. Enter your API Key in Environment Variable or on the Web App

5. After all the set up, open Command Prompt and go to the direcotry where insight_ai.py located in

6. Run the Streamlit app
   ```sh
   Streamlit run insight_ai.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Given OpenAI API Key is input on the sidebar or environment variable

Data Agent:
1. Users enter the question they want to get answer from the data into Data Agent
2. Users click Submit
3. Data Agent feeback by a dataset that can respond to the question
4. Data Agent pass the dataset to Visual Analyzer and BI Wizard, in case user want to further analyze the case

Visual Analyzer:
1. If there is no dataset from Data Agent, user can upload a data file by CSV
2. Data will then be loaded into a dashboard builder for data quality checking, data cleaning, data discovery, creating dashboard etc.

BI Wizard:
1. User enter a prompt to the BI Wizard to generate a desired visual for analysis
2. User click Generate
3. BI Wizard return a diagram according to the instruction and also a text explanation of the diagram generated
   
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [ ] More LLM Model options
- [ ] More SQL Database options
- [ ] Authorization Mechanism
- [ ] Dynamic Database Connection
- [ ] Dashboard Directory
- [ ] Advanced RAG
- [ ] Finetune, e.g. RLHF, HyDE


See the [open issues](https://github.com/micky0919/insight-ai/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Insight AI is released under the **MIT License**. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Linkedin - https://www.linkedin.com/in/micky-wong/ 

Email - wailok_0919@hotmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/micky0919/insight-ai.svg?style=for-the-badge
[contributors-url]: https://github.com/micky0919/insight-ai/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/micky0919/insight-ai.svg?style=for-the-badge
[forks-url]: https://github.com/micky0919/insightt-ai/network/members
[stars-shield]: https://img.shields.io/github/stars/micky0919/insight-ai.svg?style=for-the-badge
[stars-url]: https://github.com/micky0919/insight-ai/stargazers
[issues-shield]: https://img.shields.io/github/issues/micky0919/insight-ai.svg?style=for-the-badge
[issues-url]: https://github.com/micky0919/insight-ai/issues
[license-shield]: https://img.shields.io/github/license/micky0919/insight-ai.svg?style=for-the-badge
[license-url]: https://github.com/micky0919/insight-ai/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/micky-wong/
[product-screenshot]: images/screenshot.png
