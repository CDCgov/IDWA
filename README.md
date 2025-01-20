# Table of Contents
[1. Overview](#1-overview)
- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Future Considerations](#future-considerations)

[2. Infrastructure Architecture](#2-infrastructure-architecture)

[3. Notices](#3-notices)
- [3.1 Privacy Standard Notice](#31-privacy-standard-notice)
- [3.2 Records Management Standard Notice](#32-records-management-standard-notice)
- [3.3 Domestic Copyright Protection Notice](#33-domestic-copyright-protection-notice)
- [3.4 Public Domain Standard Notice](#34-public-domain-standard-notice)
- [3.5 Open Source Notice](#35-open-source-notice)
- [3.6 License Standard Notice](#36-license-standard-notice)
- [3.7 Github Notice](#37-github-notice)
- [3.8 Contributing Standard Notice](#38-contributing-standard-notice)

[4. General Disclaimer](#4-general-disclaimer)

[5. Other Related Documents](#5-other-related-documents)


# 1. Overview
The Intelligent Data Workflow Automation (IDWA) ReportVision Project aims to support the Office of Public Health Data, Surveillance, and Technology (OPHDST) in enhancing the ability of state, local, territorial, and tribal public health departments to manage, search, and secure critical data. As a key division of the CDC, OPHDST plays a vital role in public health infrastructure.

Please see the [UserGuide](/docs/user_guide.md) to get a technical overview of this project.

## The Problem

The exchange of public health data is hindered by outdated, manual processes. Some state, local, tribal, and territorial health departments still rely on fax, email, and physical mail to receive case data, requiring staff to manually review and re-enter information from lab reports. This labor-intensive process can take up to 20 minutes per report, and electronic data extraction remains cumbersome and error-prone, particularly when handling multiple documents. As a result, low accuracy in data ingestion impedes the ability of public health departments to efficiently process and utilize critical health data.

## The Solution

ReportVision is a powerful tool designed to automate the reading and extracting of data from lab reports, helping public health departments streamline their workflows.  Leveraging the power of the Tesseract engine and Microsoft Azure Cloud Platform, ReportVision allows teams to create customizable, data-driven templates for automatic extraction and annotation of multiple datasets—delivering notable accuracy and speed.

The goal is simple yet powerful: to provide jurisdictions with a "starter kit" that empowers them to rapidly build their own resources, provision scalable Azure infrastructure, or seamlessly replicate similar configurations in Amazon Web Services (AWS) or Google Cloud Platform (GCP).

With ReportVision, public health departments can move from cumbersome, error-prone processes to a highly efficient, automated workflow that supports critical decision-making with fast, reliable data.

This application offers a robust framework for public health departments and personnel to efficiently extract relevant data from lab reports utilizing an advanced Optical Character Recognition (OCR) model.  This OCR technology significantly enhances both the speed and accuracy of data extraction, taking your data processing capabilities to the next level.  

Check out the following video which demos the ReportVision application including how the updated OCR model works in action, and witness firsthand how ReportVision enhances both the speed and accuracy of data extraction!

https://github.com/user-attachments/assets/5b707ec2-5d11-436b-a270-98000ef21e8f

## Future Considerations

The current version of the application is optimized only for PDF-based lab reports. However, as demand from public health departments and personnel continues to grow, we see significant potential to expand support for additional file formats in future updates.

+ [Return to Table of Contents](#table-of-contents).

# 2. Infrastructure Architecture

The following provides a High-Level Architectural Design of the ReportVision Azure Architecture, with OCR powered by Tesseract to enhance efficiency, user experience, and throughput.

<img width="985" alt="rv-azure-architecture-diagram" src="https://github.com/user-attachments/assets/d27c9b63-c6b5-466f-a83f-765251252990" />

+ [Return to Table of Contents](#table-of-contents).

# 3 Notices

## 3.1 Privacy Standard Notice
This repository contains only non-sensitive, publicly available data and information. All material and community participation is covered by the [Disclaimer](DISCLAIMER.md) and [Code of Conduct](code-of-conduct.md).

For more information about CDC's privacy policy, please visit [http://www.cdc.gov/other/privacy.html](https://www.cdc.gov/other/privacy.html).

+ [Return to Table of Contents](#table-of-contents).

## 3.2 Records Management Standard Notice

This repository is not a source of government records, but is a copy to increase
collaboration and collaborative potential. All government records will be
published through the [CDC web site](http://www.cdc.gov).

+ [Return to Table of Contents](#table-of-contents).


## 3.3 Domestic Copyright Protection Notice

This repository is a work of the United States Government and is not subject to domestic copyright protection under 17 U.S.C. § 105. If published in the public domain within the United States, copyright and related rights worldwide will be waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

+ [Return to Table of Contents](#table-of-contents).

## 3.4 Public Domain Standard Notice
This repository constitutes a work of the United States Government and is not
subject to domestic copyright protection under 17 USC § 105. This repository is in
the public domain within the United States, and copyright and related rights in
the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
All contributions to this repository will be released under the CC0 dedication. By
submitting a pull request you are agreeing to comply with this waiver of
copyright interest.

+ [Return to Table of Contents](#table-of-contents).

## 3.5 Open Source Notice

This repository is open source and follows [open practices](docs/open_practices.md).  Contributors are expected to adhere to the organization's [rules of behavior](docs/rules_of_behavior.md).  

+ [Return to Table of Contents](#table-of-contents).

## 3.6 License Standard Notice

The code in this repository is licensed under the Apache License 2.0 (ASL v2), or any later version at your discretion.

You are free to use, redistribute, and modify the source code under the terms of the Apache License 2.0. However, this software is distributed "as is", without any warranties of any kind, either express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, or non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

For full licensing details, refer to the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).

Additionally, any code forked from this open-source project will retain its original license.

+ [Return to Table of Contents](#table-of-contents).

## 3.7 Github Notice

GitHub is not hosted by the CDC, but is a third party website used by CDC and its partners to share information and collaborate on software. CDC use of GitHub does not imply an endorsement of any one particular service, product, or enterprise. If you are new to GitHub, we recommend starting with this
[basic tutorial](https://help.github.com/articles/set-up-git) to familiarize yourself with version control and collaboration.  

+ [Return to Table of Contents](#table-of-contents).

## 3.8 Contributing Standard Notice

While we encourage continuous development of this repository's codebase, there is currently no designated department overseeing its management. If you'd like to contribute, you have two options:

1. Clone the repository and create a new repository in your organization's codebase with the changes you wish to implement.
   - This option allows you to manage the changes independently within your own organization's environment.
2. Submit a pull request and contact the CDC to inquire whether a department has been assigned to manage the repository.
   - If a CDC department is designated, you can coordinate with them for further changes.
   - _Note_: All comments, messages, pull requests, and other submissions received through
CDC including this GitHub page may be subject to applicable federal law, including but not limited to the Federal Records Act, and may be archived. Learn more at [http://www.cdc.gov/other/privacy.html](http://www.cdc.gov/other/privacy.html).
   - Also see [CONTRIBUTING.md](docs/CONTRIBUTING.md) and [CDC Managed Repository Guidance](#4-cdc-managed-repository-guidance).

+ [Return to Table of Contents](#table-of-contents).

# 4. General Disclaimer

This repository was created for use by CDC programs to collaborate on public health related projects in support of the [CDC mission](https://www.cdc.gov/about/cdc/?CDC_AAref_Val=https://www.cdc.gov/about/organization/mission.htm).  

+ [Return to Table of Contents](#table-of-contents).

# 5. Other Related Documents

* [Open Practices](docs/open_practices.md)
* [Rules of Behavior](docs/rules_of_behavior.md)
* [Disclaimer](docs/DISCLAIMER.md)
* [Contribution Notice](docs/CONTRIBUTING.md)
* [Code of Conduct](docs/code-of-conduct.md)
* [Review Guidelines](docs/REVIEW_GUIDELINES.md)
* [Review SLAS](docs/REVIEW_SLAS.md)
