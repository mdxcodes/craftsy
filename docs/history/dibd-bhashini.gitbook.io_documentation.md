# Table of Contents

- [Overall Understanding of the API Calls | Bhashini APIs](#overall-understanding-of-the-api-calls-bhashini-apis)
- [Overall Understanding of the API Calls | Bhashini APIs](#overall-understanding-of-the-api-calls-bhashini-apis)
- [Pre-requisites and Onboarding | Bhashini APIs](#pre-requisites-and-onboarding-bhashini-apis)
- [Pipeline Search Call | Bhashini APIs](#pipeline-search-call-bhashini-apis)
- [Available Models for usage | Bhashini APIs](#available-models-for-usage-bhashini-apis)
- [Pipeline Config Call | Bhashini APIs](#pipeline-config-call-bhashini-apis)
- [Pipeline Compute Call | Bhashini APIs](#pipeline-compute-call-bhashini-apis)
- [Request Payload | Bhashini APIs](#request-payload-bhashini-apis)
- [Transliteration Config Call | Bhashini APIs](#transliteration-config-call-bhashini-apis)
- [Transliteration Compute Call | Bhashini APIs](#transliteration-compute-call-bhashini-apis)
- [Request Payload | Bhashini APIs](#request-payload-bhashini-apis)
- [Response Payload | Bhashini APIs](#response-payload-bhashini-apis)
- [Response Payload | Bhashini APIs](#response-payload-bhashini-apis)
- [Request Payload | Bhashini APIs](#request-payload-bhashini-apis)
- [Optical Character Recognition Call | Bhashini APIs](#optical-character-recognition-call-bhashini-apis)
- [Request Payload | Bhashini APIs](#request-payload-bhashini-apis)
- [Text Language Detection Compute Call | Bhashini APIs](#text-language-detection-compute-call-bhashini-apis)
- [Request payload | Bhashini APIs](#request-payload-bhashini-apis)
- [Request Payload | Bhashini APIs](#request-payload-bhashini-apis)
- [Download Postman Collection | Bhashini APIs](#download-postman-collection-bhashini-apis)
- [Request Payload | Bhashini APIs](#request-payload-bhashini-apis)
- [WebSocket ASR API | Bhashini APIs](#websocket-asr-api-bhashini-apis)
- [Response Payload | Bhashini APIs](#response-payload-bhashini-apis)
- [Request Payload | Bhashini APIs](#request-payload-bhashini-apis)
- [Response Payload | Bhashini APIs](#response-payload-bhashini-apis)
- [Audio Language Detection Compute Call | Bhashini APIs](#audio-language-detection-compute-call-bhashini-apis)
- [Speaker Diarization Compute Call | Bhashini APIs](#speaker-diarization-compute-call-bhashini-apis)
- [Response Payload | Bhashini APIs](#response-payload-bhashini-apis)
- [Possible Errors | Bhashini APIs](#possible-errors-bhashini-apis)
- [Appendix | Bhashini APIs](#appendix-bhashini-apis)
- [OCR Modalities Overview | Bhashini APIs](#ocr-modalities-overview-bhashini-apis)
- [Response Payload | Bhashini APIs](#response-payload-bhashini-apis)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Response Payload | Bhashini APIs](#response-payload-bhashini-apis)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Response Payload | Bhashini APIs](#response-payload-bhashini-apis)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)
- [Unknown](#unknown)

---

# Overall Understanding of the API Calls | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/overall-understanding-of-the-api-calls.md)
.

> _**This Bhashini Documentation has been written by Bhashini Team. Please reach out to Bhashini Team on email id (**__**digitalindiabhashinidivision@gmail.com**__**), if you face issues implementing the APIs.**_

Please refer to [Appendix](https://dibd-bhashini.gitbook.io/bhashini-apis/appendix)
 for details on full forms.

### What models are available on ULCA?[](https://dibd-bhashini.gitbook.io/#what-models-are-available-on-ulca)

Our Research and Development groups which comprises of different renowned institutes of India like IIT(s), IIIT(s), CDAC etc. have developed models which can do Speech Recognition, Translations, Text to Speech, Optical Character Recognition and many more for Indian languages. Our ULCA Platform exposes these AI/ML models (each identified with an unique Model ID) and a try out page through which integrators can try these models.

[![Logo](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2Fbhashini.gov.in%2Fulca%2Fmodel%2Ffavicon.ico&width=20&dpr=3&quality=100&sign=8cd8ba2b813c8a870ba5a19205be2977&sv=3)Bhashinibhashini.gov.in](https://bhashini.gov.in/ulca/model/explore-models)

ULCA Repository of Models

Multiple models could be available that may have similar functionality. For ex. To do Speech Recognition of Hindi language, there may be multiple models available from different institute each uniquely identified by a model ID.

What is a ULCA pipeline?[](https://dibd-bhashini.gitbook.io/#what-is-a-ulca-pipeline)

--------------------------------------------------------------------------------------

ULCA Pipeline is a set of tasks that any specific pipeline supports. For example, any specific pipeline (identified by unique pipeline ID) can support the following:

What is Pipeline ID?[](https://dibd-bhashini.gitbook.io/#what-is-pipeline-id)

------------------------------------------------------------------------------

*   Another pipeline `P2`, may support only following Tasks and Task Sequences: `[NMT]` `[TTS]` `[NMT+TTS]`
    

When to use which Pipeline ID?[](https://dibd-bhashini.gitbook.io/#when-to-use-which-pipeline-id)

--------------------------------------------------------------------------------------------------

Consider Bhashini provides a few pipelines `(pipeline ID: P1, P2, etc.)` that supports some Tasks and Task Sequences.

**Case 1:** If the use case is to do only Translation where an integrator wants to translate a given sentence from one language to another in their app/project. For this use case, a pipeline which supports `[NMT]` shall be used. Since pipeline `P1` and `P2` both supports `[NMT]` task, either `P1` or `P2` can be used. **Case 2:** Consider another use case, where integrator would also want its users to be able to hear the output along with reading which would require both `NMT` and `TTS` to be done on the input text, integrator will need a pipeline that supports `[NMT+TTS]`. Since pipeline `P1` and `P2` both supports `[NMT+TTS]`, either `P1` or `P2` can be used. **Case 3:** Consider yet another use case, where integrator wants to take the input in the form of voice and provide a translated text from one language to another. Integrator will, in this case, needs a pipeline which supports `[ASR+NMT]`. Since only Pipeline `P1` supports `ASR` and `NMT` together, only `P1` can be used.

**Case 4:** Consider yet another use case, where the integrator wants to utilize ASR from Pipeline `P1` and `[NMT]` from Pipeline `P2`. The integrator can achieve this as long as both pipelines point to the same API endpoint and are accessible with the same Authorization Keys. Now, from Case 1 and 2, question arises, which one to use, since both are able to do the required task? Integrators will have a detailed description of the capabilities of the pipeline, the models used in those pipelines, domains to which this pipeline may cater well. e.g. Certain pipelines are made for Medical Domain compared to some other pipeline which may cater to Agriculture domain better. Along with description, there is a Search Pipeline API call as well which provides similar information for automation purposes. Based on the understanding obtained from the portal as well as information obtained from the API, the integrator shall be able to determine which pipeline ID to use if multiple pipelines are available which does the same Tasks/Task Sequences.

Each of these pipelines are uniquely identified by Pipeline ID.

Each pipeline can support multiple and/or combination of tasks.

In each of the Task Sequences, order/sequence of tasks is important. e.g. If a pipeline supports `[ASR+NMT+TTS]`, it will mean that on the input received, first speech recognition will be done, then it will be translated to another language following which Speech in the target language will be generated.

Flow of API calls[](https://dibd-bhashini.gitbook.io/#flow-of-api-calls)

-------------------------------------------------------------------------

Integrator shall do following calls to get the output.

#### [Pipeline Search API Call \[Optional\]](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call)
[](https://dibd-bhashini.gitbook.io/#pipeline-search-api-call-optional)

Pipeline Search API Call helps the integrator to search for pipelines that are available to do specific Tasks or Task Sequences and can be used to filter pipeline search based on different parameters. Integrators will be able to obtain `Pipeline IDs` required for their project using this call.

#### Pipeline Config Call \[Mandatory\][](https://dibd-bhashini.gitbook.io/#pipeline-config-call-mandatory)

Once the integrator obtains the Pipeline ID either via Search Call or ULCA web portal, Pipeline Config call shall be sent to Bhashini along with the specific Task/Task Sequence that integrator want to do using this pipeline. Integrator should make sure that the sequence they are sending shall be supported by this pipeline. There are additional configuration parameters which integrators may or may not send to further filter the response of this config call.

#### Pipeline Compute Call \[Mandatory\][](https://dibd-bhashini.gitbook.io/#pipeline-compute-call-mandatory)

Pipeline Compute Call is the final call that will help the integrator to obtain the output of the pipeline task sent.

Language Codes[](https://dibd-bhashini.gitbook.io/#language-codes)

-------------------------------------------------------------------

Throughout the APIs, Integrators will see that languages are referred by their language codes. For ex. Language Code for Hindi is hi, English is en, and so on.

Bhashini follows [ISO-639 series](https://www.loc.gov/standards/iso639-2/php/code_list.php)
 of language codes.

Usage of these APIs shall be for the purposes of PoC only. If the Bhashini Sahyogi, Bhashini App Mitra or Bhashini Udyat Mitra wants to use the same on production systems or integrators are charging end-users, please reach out to Bhashini team for the paid version of the APIs and exploring Pricing Plans.

[NextPre-requisites and Onboarding](https://dibd-bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding)

Last updated 1 year ago

---

# Overall Understanding of the API Calls | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/overall-understanding-of-the-api-calls.md)
.

> _**This Bhashini Documentation has been written by Bhashini Team. Please reach out to Bhashini Team on email id (**__**digitalindiabhashinidivision@gmail.com**__**), if you face issues implementing the APIs.**_

Please refer to [Appendix](https://dibd-bhashini.gitbook.io/bhashini-apis/appendix)
 for details on full forms.

### What models are available on ULCA?[](https://dibd-bhashini.gitbook.io/bhashini-apis#what-models-are-available-on-ulca)

Our Research and Development groups which comprises of different renowned institutes of India like IIT(s), IIIT(s), CDAC etc. have developed models which can do Speech Recognition, Translations, Text to Speech, Optical Character Recognition and many more for Indian languages. Our ULCA Platform exposes these AI/ML models (each identified with an unique Model ID) and a try out page through which integrators can try these models.

[![Logo](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2Fbhashini.gov.in%2Fulca%2Fmodel%2Ffavicon.ico&width=20&dpr=3&quality=100&sign=8cd8ba2b813c8a870ba5a19205be2977&sv=3)Bhashinibhashini.gov.in](https://bhashini.gov.in/ulca/model/explore-models)

ULCA Repository of Models

Multiple models could be available that may have similar functionality. For ex. To do Speech Recognition of Hindi language, there may be multiple models available from different institute each uniquely identified by a model ID.

What is a ULCA pipeline?[](https://dibd-bhashini.gitbook.io/bhashini-apis#what-is-a-ulca-pipeline)

---------------------------------------------------------------------------------------------------

ULCA Pipeline is a set of tasks that any specific pipeline supports. For example, any specific pipeline (identified by unique pipeline ID) can support the following:

What is Pipeline ID?[](https://dibd-bhashini.gitbook.io/bhashini-apis#what-is-pipeline-id)

-------------------------------------------------------------------------------------------

*   Another pipeline `P2`, may support only following Tasks and Task Sequences: `[NMT]` `[TTS]` `[NMT+TTS]`
    

When to use which Pipeline ID?[](https://dibd-bhashini.gitbook.io/bhashini-apis#when-to-use-which-pipeline-id)

---------------------------------------------------------------------------------------------------------------

Consider Bhashini provides a few pipelines `(pipeline ID: P1, P2, etc.)` that supports some Tasks and Task Sequences.

**Case 1:** If the use case is to do only Translation where an integrator wants to translate a given sentence from one language to another in their app/project. For this use case, a pipeline which supports `[NMT]` shall be used. Since pipeline `P1` and `P2` both supports `[NMT]` task, either `P1` or `P2` can be used. **Case 2:** Consider another use case, where integrator would also want its users to be able to hear the output along with reading which would require both `NMT` and `TTS` to be done on the input text, integrator will need a pipeline that supports `[NMT+TTS]`. Since pipeline `P1` and `P2` both supports `[NMT+TTS]`, either `P1` or `P2` can be used. **Case 3:** Consider yet another use case, where integrator wants to take the input in the form of voice and provide a translated text from one language to another. Integrator will, in this case, needs a pipeline which supports `[ASR+NMT]`. Since only Pipeline `P1` supports `ASR` and `NMT` together, only `P1` can be used.

**Case 4:** Consider yet another use case, where the integrator wants to utilize ASR from Pipeline `P1` and `[NMT]` from Pipeline `P2`. The integrator can achieve this as long as both pipelines point to the same API endpoint and are accessible with the same Authorization Keys. Now, from Case 1 and 2, question arises, which one to use, since both are able to do the required task? Integrators will have a detailed description of the capabilities of the pipeline, the models used in those pipelines, domains to which this pipeline may cater well. e.g. Certain pipelines are made for Medical Domain compared to some other pipeline which may cater to Agriculture domain better. Along with description, there is a Search Pipeline API call as well which provides similar information for automation purposes. Based on the understanding obtained from the portal as well as information obtained from the API, the integrator shall be able to determine which pipeline ID to use if multiple pipelines are available which does the same Tasks/Task Sequences.

Each of these pipelines are uniquely identified by Pipeline ID.

Each pipeline can support multiple and/or combination of tasks.

In each of the Task Sequences, order/sequence of tasks is important. e.g. If a pipeline supports `[ASR+NMT+TTS]`, it will mean that on the input received, first speech recognition will be done, then it will be translated to another language following which Speech in the target language will be generated.

Flow of API calls[](https://dibd-bhashini.gitbook.io/bhashini-apis#flow-of-api-calls)

--------------------------------------------------------------------------------------

Integrator shall do following calls to get the output.

#### [Pipeline Search API Call \[Optional\]](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call)
[](https://dibd-bhashini.gitbook.io/bhashini-apis#pipeline-search-api-call-optional)

Pipeline Search API Call helps the integrator to search for pipelines that are available to do specific Tasks or Task Sequences and can be used to filter pipeline search based on different parameters. Integrators will be able to obtain `Pipeline IDs` required for their project using this call.

#### Pipeline Config Call \[Mandatory\][](https://dibd-bhashini.gitbook.io/bhashini-apis#pipeline-config-call-mandatory)

Once the integrator obtains the Pipeline ID either via Search Call or ULCA web portal, Pipeline Config call shall be sent to Bhashini along with the specific Task/Task Sequence that integrator want to do using this pipeline. Integrator should make sure that the sequence they are sending shall be supported by this pipeline. There are additional configuration parameters which integrators may or may not send to further filter the response of this config call.

#### Pipeline Compute Call \[Mandatory\][](https://dibd-bhashini.gitbook.io/bhashini-apis#pipeline-compute-call-mandatory)

Pipeline Compute Call is the final call that will help the integrator to obtain the output of the pipeline task sent.

Language Codes[](https://dibd-bhashini.gitbook.io/bhashini-apis#language-codes)

--------------------------------------------------------------------------------

Throughout the APIs, Integrators will see that languages are referred by their language codes. For ex. Language Code for Hindi is hi, English is en, and so on.

Bhashini follows [ISO-639 series](https://www.loc.gov/standards/iso639-2/php/code_list.php)
 of language codes.

Usage of these APIs shall be for the purposes of PoC only. If the Bhashini Sahyogi, Bhashini App Mitra or Bhashini Udyat Mitra wants to use the same on production systems or integrators are charging end-users, please reach out to Bhashini team for the paid version of the APIs and exploring Pricing Plans.

[NextPre-requisites and Onboarding](https://dibd-bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding)

Last updated 1 year ago

---

# Pre-requisites and Onboarding | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding.md)
.

Account Creation[](https://dibd-bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding#account-creation)

------------------------------------------------------------------------------------------------------------------

Integrator shall onboard themselves on Bhashini via the link below: Registration: [https://dashboard.bhashini.co.in/user/register](https://dashboard.bhashini.co.in/user/register)

Once an Integrator reaches the Integrator Registration Page, Integrator has to fill the required details as shown below:

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Fuploads%252FUTt5kbnBCHGu9BG7JPI6%252FScreenshot%25202025-02-06%2520145922.png%3Falt%3Dmedia%26token%3D225c6cd6-60a8-47a8-aeab-40f1c9db9a82&width=768&dpr=3&quality=100&sign=be7acb077ab6fdea6c7ac6e649e3039a&sv=3)

Please check the spam folder for authentication email too.

Users will be able to view their USER ID, API Keys once registered and the registration of the account is approved by DIBD team.

[PreviousOverall Understanding of the API Calls](https://dibd-bhashini.gitbook.io/bhashini-apis)
[NextAvailable Models for usage](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage)

Last updated 1 year ago

---

# Pipeline Search Call | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call.md)
.

Currently, 4 pipeline IDs are available to used directly as follows:

*   IIT Madras Models: 660fa5bec7fb5b0328229016 \[ASR and TTS task types are available in config call for now\]
    
*   IIT Bombay Models: 660f813c0413087224435d2c \[Translation task type are available in config call for now\]
    
*   IIIT Hyderabad Models: 660f866443e53d4133f65317 \[Translation task type are available in config call for now\]
    
*   Initial Pipeline Models: 64392f96daac500b55c543cd \[ASR, Translation, Transliteration and TTS task types are available in config call for now\]
    

[PreviousAvailable Models for usage](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage)
[NextPipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)

Last updated 1 year ago

---

# Available Models for usage | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage.md)
.

The list below consists of Service ID's to be utilized, each Service ID helps connect with a specific model via the REST APIs of Bhashini. The Service ID's, task type supported by it (such as ASR, Translation, TTS, etc) and the languages supported by it are listed below.

ASR[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#asr)

-------------------------------------------------------------------------------------

Sl. No

Service ID

Language(s) Supported

Model Provider

1

bhashini/iitm/asr-dravidian--gpu--t4

Telugu, Kannada, Malayalam, Tamil

IIT Madras

2

ai4bharat/conformer-hi-gpu--t4

Hindi

AI4Bharat

3

ai4bharat/conformer-multilingual-dravidian-gpu--t4

Kannada, Malayalam, Tamil, Telugu

AI4Bharat

4

ai4bharat/conformer-multilingual-indo\_aryan-gpu--t4

Hindi, Bengali, Marathi, Urdu, Odia, Punjabi, Gujarati, Sanskrit

AI4Bharat

5

ai4bharat/whisper-medium-en--gpu--t4

English

AI4Bharat

6

bhashini/ai4bharat/conformer-multilingual-asr

Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmir, Goan Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu

AI4Bharat

7

bhashini/iitm/asr-indoaryan--gpu--t4

Gujarati, Odia, Hindi, Marathi, Punjabi, Bengali

IIT Madras

8

bhashini/iitm/asr-misc--gpu--t4

Bhojpuri, Urdu

IIT Madras

9

bhashini/iisc/asr-mai-t4

Maithili

IISC

10

bhashini/iisc/asr-bho-t4

Bhojpuri

IISC

11

bhashini/bodhan/asr-transcribe-flex

English, Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu, Bhojpuri, Chhattisgarhi, Haryanvi, Bhili

Bodhan.AI

12

bhashini/bodhan/asr-transcribe-core

English, Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu, Bhojpuri, Bhili

Bodhan.AI

Translation[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#translation)

-----------------------------------------------------------------------------------------------------

Sl. No

Service ID

Source Language(s) Supported

Target Language(s) Supported

Model Provider

1

bhashini/iiith/nmt-all

Hindi, English, Assamese, Awadhi, Bengali, Bhojpuri, Braj, Bodo, Dogri, Konkani, Gondi, Gujarati, Hinglish, Ho, Kannada, Kashmiri, Khasi, Mizo, Maithili, Magahi, Malayalam, Marathi, Manipuri, Nepali, Oriya, Punjabi, Sanskrit, Santali, Sinhala, Sindhi, Tamil, Tulu, Telugu, Urdu, Kangri, Kashmiri

Hindi, English, Assamese, Awadhi, Bengali, Bhojpuri, Braj, Bodo, Dogri, Konkani, Gondi, Gujarati, Hinglish, Ho, Kannada, Kashmiri, Khasi, Mizo, Maithili, Magahi, Malayalam, Marathi, Manipuri, Nepali, Oriya, Punjabi, Sanskrit, Santali, Sinhala, Sindhi, Tamil, Tulu, Telugu, Urdu, Kangri, Kashmiri

IIIT Hyderabad

2

ai4bharat/indictrans-v2-all-gpu--t4

English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali

English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali

AI4Bharat

3

Bhashini/IIITH/Trans/V1

Hindi, English, Telugu, Odia, Gujarati, Urdu,

Punjabi, Hindi, English, Telugu, Urdu, Gujarati, Odia, Sindhi, Dogri, Kashmiri

IIIT Hyderabad

4

iitb/trilingual-en\_hi\_mr-v1-gpu--t4

English, Assamese, Marathi, Hindi

Assamese, Hindi, Bodo, Nepali, English, Marathi, Maithili, Goan Konkani

IIT Bombay

5

bhashini/aukbc/disco-nmt

Malayalam, Hindi, Tamil

Malayalam, Hindi, Tamil

AUKBC

6

bhashini/cdac-noida/nmt

English, Hindi, Tamil, Odia , Bengali

English, Hindi, Tamil, Odia , Bengali

CDAC-Noida

7

bhashini/cdac-pune/nmt

English, Kannada, Gujarati,Malayalam

English, Kannada, Gujarati, Malayalam

CDAC-Pune

8

bhashini/iitkhg/nmt

Hindi

Sanskrit

IIT Kharagpur

9

bhashini/bodhan/Indic-trans-v4

English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali

English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali

Bodhan.AI

10

bhashini/iiith/santham/nmt

Sanskrit

Tamil

IIITH

Transliteration[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#transliteration)

-------------------------------------------------------------------------------------------------------------

Sl. No

Service ID

Source Language(s) Supported

Target Language(s) Supported

Model Provider

1

ai4bharat/indicxlit--cpu-fsv2

English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali, Punjabi, Maithili, Urdu, Sinhala, Bodo,

English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali, Punjabi, Maithili, Urdu, Sinhala, Bodo

AI4Bharat

TTS[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#tts)

-------------------------------------------------------------------------------------

Sl. No

Service ID

Language(s) Supported

Model Provider

1

Bhashini/IITM/TTS

Assamese, Bengali, Bodo, Dogri, English, Gujarati, Hindi, Kannada, Goan Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Rajasthani, Sanskrit, Tamil, Telugu, Urdu, Santali (Devanagari Script), Sindhi(Devanagari Script), Kashmiri(Devanagari Script)

IIT Madras

2

ai4bharat/indic-tts-coqui-dravidian-gpu--t4

Malayalam, Kannada, Tamil, Telugu

AI4Bharat

3

ai4bharat/indic-tts-coqui-indo\_aryan-gpu--t4

Hindi, Marathi, Assamese, Bengali, Gujarat, Odia, Rajasthani, Punjabi

AI4Bharat

4

ai4bharat/indic-tts-coqui-misc-gpu--t4

English, Manipuri, Bodo

AI4Bharat

5

Bhashini/IISC/TTS

Kannada, Telugu, English, Hindi, Marathi, Bengali, Gujarati, Maithili, Bhojpuri, Chhattisgarhi, Magahi

IISC (SYSPIN)

6

bhashini/iisc/sourashtra/tts

Sourashtra, Tamil

IISC

7

bhashini/bodhan/indic-tts

English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali

Bodhan.AI

Audio Language Detection[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#audio-language-detection)

-------------------------------------------------------------------------------------------------------------------------------

Sl. No

Service ID

Language(s) Supported

Model Provider

1

bhashini/iitmandi/audio-lang-detection/gpu

Assamese, Bengali, English, Hindi, Kannada, Gujarati, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu

IIT Mandi

2

bhashini/ald

Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali

\-

Text Language Detection[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#text-language-detection)

-----------------------------------------------------------------------------------------------------------------------------

Sl. No

Service ID

Language(s) Supported

Model Provider

1

bhashini/indic-lang-detection-all

Assamese, Bengali, Bodo, Dogri, English, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Oriya, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu

AI4Bharat

2

bhashini/iiiith/indic-lang-detection-all

Assamese, Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Manipuri, Marathi, Oriya, Punjabi, Tamil, Telugu, Urdu

IIIT Hyderabad

3

bhashini/indic/tld

Assamese(bng script), Bodo, Bangla, Dogri, English, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu

\-

Named Entity Recognition[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#named-entity-recognition)

-------------------------------------------------------------------------------------------------------------------------------

Sl. No

Service ID

Language(s) Supported

Model Provider

1

bhashini/iiith/ner

Hindi, Urdu, Odia, Telugu

IIIT Hyderabad

2

bhashini/ai4bharat/indic-ner

Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Telugu, Marathi, Oriya, Punjabi, Tamil

AI4Bharat

3

bhashini/aukbc/ner

Hindi, Bengali, Marathi, Punjabi, Kannada, Malayalam, Tamil, English

AUKBC

OCR[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#ocr)

-------------------------------------------------------------------------------------

Sl. No

Service ID

Language(s) Supported

Modality

Model Provider

1

bhashini/iiith-ocr-sceneText-all

Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Manipuri, Marathi, Oriya, Punjabi, Tamil, Telugu, Urdu

Scene Text

IIIT Hyderabad

2

bhashini/iiith/ocr-hw-bhaasha

Bengali, Hindi, Malayalam, Marathi, Punjabi, Telugu, Kannada, Tamil

Handwritten

IIIT Hyderabad

3

bhashini/iiith-bhasha-ocr

Assamese, Bengali, Bodo, Dogri, English, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithali, Nepali, Malayalam, Manipuri, Marathi, Oriya, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu

Printed Text

IIIT Hyderabad

4

bhashini/bodhan/indic-doc/ocr

English, Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu.

Printed Text

Bodhan.AI

5

bhashini/bodhan/indic-doc/ocr

English, Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Kannada, Malayalam, Odia, Punjabi, Assamese, Urdu.

Handwritten Text

Bodhan.AI

Speaker Enrollment & Verification[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#speaker-enrollment-and-verification)

---------------------------------------------------------------------------------------------------------------------------------------------------

SI.No

Service ID

Language(s) Supported

Model Provider

1

bhashini/iitdharwad/speaker-enrollment

All Languages

IIT Dharwad

2

bhashini/iitdharwad/speaker-verification

All Languages

IIT Dharwad

Speaker Diarization[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#speaker-diarization)

---------------------------------------------------------------------------------------------------------------------

SI.No

Service ID

Language(s) Supported

Model Provider

1

bhashini/iisc/speaker-diarization

All Languages

IISC

2

bhashini/speaker-diarization

All Languages

Open Source

Language Diarization[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#language-diarization)

-----------------------------------------------------------------------------------------------------------------------

S.No

Service ID

Language(s) Supported

Model Provider

1

bhashini/nitk/language-diarization

All Languages

NITK

Voice Cloning[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#voice-cloning)

---------------------------------------------------------------------------------------------------------

S.No

Service ID

Language(s) Supported

Model Provider

1

bhashini/ai4b/indicf5-tts

Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu.

AI4Bharat

Lip Sync[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#lip-sync)

-----------------------------------------------------------------------------------------------

S.No

Service ID

Language(s) Supported

Model Provider

1

bhashini/iitm/lip-sync

All Languages

IIT Madras

KWS (Key-Word Spotting)[](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage#kws-key-word-spotting)

---------------------------------------------------------------------------------------------------------------------------

S.No

Service ID

Language(s) Supported

Model Provider

1

bhashini/iitg/kws

Bengali, Manipuri, Mizo

IIT Guwahati

[PreviousPre-requisites and Onboarding](https://dibd-bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding)
[NextPipeline Search Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call)

Last updated 1 day ago

---

# Pipeline Config Call | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call.md)
.

**Endpoint:** [https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline](https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline)

**Additional Headers:**

*   userID
    
*   ulcaApiKey
    

**Payload:**

*   [Tab 1: JSON payload without any configuration parameters](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)
    
*   [Tab 2: JSON payload with some configuration parameters](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#with-configuration-parameters)
    

Additional Headers[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call#additional-headers)

-------------------------------------------------------------------------------------------------------------

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage. `**userID:**` Uniquely identify the Integrator. `**ulcaApiKey:**` to Authenticate this particular userID

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, **userID** and **ulcaApiKey** are the additional parameters sent.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252FOJuSinbl0qQ6CBddwwe8%252Fimage.png%3Falt%3Dmedia%26token%3Dc5cbeadb-8cb2-4949-802c-64e3de0bbf8d&width=768&dpr=3&quality=100&sign=8aeaa7049716da68249a4bb34e5f9ca6&sv=3)

Postman screenshot of additional parameters

Both userID and ulcaApiKey can be obtained from the **My Profile** section after logging in.

[PreviousPipeline Search Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call)
[NextRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)

Last updated 1 year ago

---

# Pipeline Compute Call | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call.md)
.

**Endpoint:** Endpoint is obtained from the `**callbackURL**` parameter under [`**pipelineInferenceAPIEnfPoint**`](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)
 parameter from the Response Payload of [Pipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
 as shown [here.](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)

**Additional Headers:** auth parameter key auth parameter value

**Payload:**

*   ASR
    
*   Translation
    
*   TTS
    
*   ASR+Translation
    
*   Translation+TTS
    
*   ASR+Translation+TTS
    

Additional Headers[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call#additional-headers)

--------------------------------------------------------------------------------------------------------------

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Compute API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage. **auth parameter key**: This value is obtained from `**name**` parameter under `**inferenceApiKey**` under [`**pipelineInferenceAPIEnfPoint**`](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)
.

**auth parameter value**: This value is obtained from `**value**` parameter under `**inferenceApiKey**` under [`**pipelineInferenceAPIEnfPoint**`](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)
.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Fuploads%252Fv9Il636tmGhrOQvqNp0C%252Fspaces_SuLLfCr6CWwqT0SsqOL1_uploads_0KKVeasdrDINiAvokkjE_image.webp%3Falt%3Dmedia%26token%3D954aafc0-faf1-4258-8852-4d748e31ee07&width=768&dpr=3&quality=100&sign=444f844c4659d7556ecdfbf14054e3e8&sv=3)

To know more about Additional Headers, please refer [here.](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)

[PreviousResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload)
[NextRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload)

Last updated 2 years ago

---

# Request Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload.md)
.

Without configuration parameters

With Configuration Parameters

Copy

    {
        "pipelineTasks" : [\
            {\
                "taskType" : "asr"\
            },\
            {\
                "taskType": "translation"\
            },\
            {  \
                "taskType": "tts"\
            },\
            \
        ],
        "pipelineRequestConfig" : {
            "pipelineId" : "xxxx8d51ae52cxxxxxxxx"
        }
    }

### Parameters[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#parameters)

We will now understand about each parameter available as a part of this payload. **taskType**

**Type:** String

*   Line 3-5 for ASR
    
*   Line 6-8 for Translation
    
*   Line 9-11 for TTS
    

#### pipelineTasks[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#pipelinetasks)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` as defined above, that are to be done by the integrator. The sequence of tasks matter. In the above example, the configuration that will be returned back in the response will be for tasks ASR, Translation and TTS in that order. Each `pipelineId` (discussed below), may support few individual or task sequences as explained [here](https://dibd-bhashini.gitbook.io/bhashini-apis)
 and [here](https://dibd-bhashini.gitbook.io/bhashini-apis)
 and detailed out below.

#### pipelineId[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#pipelineid)

**Type:** String `pipelineId` takes a string value of the specific pipeline integrator wants to use. The pipeline ID can be obtained either via Pipeline Search Call or via ULCA Web based on the description which helps the integrator to understand what a pipeline can or cannot do. Each pipeline ID may support multiple task and task sequences.

The same has been explained [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call)
 and [here](https://dibd-bhashini.gitbook.io/bhashini-apis)
.

#### pipelineRequestConfig[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#pipelinerequestconfig)

**Type:** Dictionary This parameter takes in the configuration requested to do the sequence of tasks defined under parameter [pipelineTasks](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#pipelinetasks)
.

### Integrators want to do individual tasks[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#integrators-want-to-do-individual-tasks)

Payload for Only ASR

Payload for Only Translation

Payload for Only TTS

`**pipelineTasks**` array takes only one dictionary with `**taskType**` as `**asr**`

Copy

    "pipelineTasks" : [\
        {\
            "taskType" : "asr"\
        }\
    ]

`**pipelineTasks**` array takes only one dictionary with `**taskType**` as `**translation**`

Copy

    "pipelineTasks" : [\
        {\
            "taskType" : "translation"\
        }\
    ]

`**pipelineTasks**` array takes only one dictionary with `**taskType**` as `**tts**`

Copy

    "pipelineTasks" : [\
        {\
            "taskType" : "tts"\
        }\
    ]

### Integrators want to do combination of tasks in that order[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#integrators-want-to-do-combination-of-tasks-in-that-order)

ASR then Translation

Translation then TTS

ASR Then Translation then TTS

`**pipelineTasks**` array takes two dictionaries with `**taskType**` as `**asr**` and `**translation**` in that sequence.

Requesting Server with this in the `**pipelineTasks**` parameter would mean that integrator wants to ask the server to give the configuration details where server will be able to perform `**ASR**` and `**Translation**` together by first doing ASR on the input audio, generating digital text of that audio and then also able to generate translation on the output of that ASR.

Copy

    "pipelineTasks" : [\
        {\
            "taskType" : "asr"\
        },\
        {\
            "taskType" : "translation"\
        }\
    ]

`**pipelineTasks**` array takes two dictionaries with `**taskType**` as `**translation**` and `**tts**` in that sequence.

Requesting Server with this in the `**pipelineTasks**` parameter would mean that integrator wants to ask the server to give the configuration details where server will be able to perform `**Translation**` and `**TTS**` together by first doing Translation on the input text, generating translated text in another language and then also able to generate Speech on the output of that translation.

Copy

    "pipelineTasks" : [\
        {\
            "taskType" : "translation"\
        },\
        {\
            "taskType" : "tts"\
        }\
    ]

`**pipelineTasks**` array takes three dictionaries with `**taskType**` as `**asr**`, `**translation**` and `**tts**` in that sequence.

Requesting Server with this in the `**pipelineTasks**` parameter would mean that integrator wants to ask the server to give the configuration details where server will be able to perform `**ASR**`, `**Translation**` and `**TTS**` together by first performing `**ASR**`, thereby generating digital text from the input audio, then doing `**Translation**` on the output of previous ASR, thereby generating digital text in another language and finally doing `**TTS**` on the output of previous Translation, thereby generating Speech in the required language.

Copy

    "pipelineTasks" : [\
        {\
            "taskType" : "asr"\
        },\
        {\
            "taskType" : "translation"\
        },\
        {\
            "taskType" : "tts"\
        }\
    ]

Copy

    {
        "pipelineTasks": [\
            {\
                "taskType": "asr",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "xx"\
                    }\
                }\
            },\
            {\
                "taskType": "translation",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "xx",\
                        "targetLanguage": "yy"\
                    }\
                }\
            },\
            {\
                "taskType": "tts",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "yy"\
                    }\
                }\
            },\
            \
        ],
        "pipelineRequestConfig": {
            "pipelineId" : "xxxx8d51ae52cxxxxxxxx"
        }
    }

### Parameters[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#parameters-1)

Only additional parameter `config` is detailed out below. Rest of the parameters' understanding remains the same as [Without configuration parameters](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#without-configuration-parameters)
.

#### config[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#config)

**Type:** dictionary `config` parameter is used for sending configuration parameters to the server for each `taskType`. Each `taskType` may have some common parameters such as `language` and some parameters which are specific to each `taskType`.

Currently, there are no additional `taskType` specific parameters. Once added, they will be described here.

#### config[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#config-1)

ASR

Translation

TTS

**Type:** dictionary

contains: **language Type:** dictionary contains: **sourceLanguage Type:** String Source Language will take the [ISO-639 code](https://bhashini.gitbook.io/bhashini-apis/)
 of the language as the input. This parameter will tell the server that integrator wants to receive the information and details about Speech Recognition in this specific language.

**Type:** dictionary

contains: **language Type:** dictionary contains: **sourceLanguage Type:** String Source Language will take the [ISO-639 code](https://bhashini.gitbook.io/bhashini-apis/)
 of the language as the input. This parameter will tell the server that integrator wants to receive the `Translation` information where the input can be translated `**FROM**` this language to another language specified in the `targetLanguage` below. and **targetLanguage Type:** String Target Language will also take the [ISO-639 code](https://bhashini.gitbook.io/bhashini-apis/)
 of the language as the input. This parameter will tell the server that integrator wants to receive the `Translation` information where the input can be translated `**TO**` this language from another language specified un the `sourceLanguage` above.

If Translation comes after ASR, and ASR is done in, say `Marathi`, then Source Language of Translation should be `Marathi` (ISO Code `mr`) because the output of ASR (Digital text in Marathi) will be fed to Translation Model. However, if Translation is the first task or the only task, integrator shall provide appropriate Source Language based on the use case.

**Type:** dictionary

contains: **language Type:** dictionary contains: **sourceLanguage Type:** String Source Language will take the [ISO-639 code](https://bhashini.gitbook.io/bhashini-apis/)
 of the language as the input. This parameter will tell the server that integrator wants to receive the information and details about converting text to speech for this specific language.

If TTS comes after Translation, and Translation is done, say from `Marathi` to `Hindi`, then Source Language of TTS should be `Hindi` (ISO Code `hi`) because the output of Translation (Translated text in Hindi) will be fed to Translation Model. However, if Translation is the first task or the only task, integrator shall provide appropriate Source Language based on the use case.

[PreviousPipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
[NextResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload)

Last updated 2 years ago

---

# Transliteration Config Call | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call.md)
.

**Endpoint:** [https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline](https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline)

**Additional Headers:**

*   userID
    
*   ulcaApiKey
    

**Payload:**

*   [Tab 1: JSON payload without any configuration parameters](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)
    
*   [Tab 2: JSON payload with some configuration parameters](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#with-configuration-parameters)
    

Additional Headers[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call#additional-headers)

--------------------------------------------------------------------------------------------------------------------

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage. `**userID:**` Uniquely identify the Integrator. `**ulcaApiKey:**` to Authenticate this particular userID

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, **userID** and **ulcaApiKey** are the additional parameters sent.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252FOJuSinbl0qQ6CBddwwe8%252Fimage.png%3Falt%3Dmedia%26token%3Dc5cbeadb-8cb2-4949-802c-64e3de0bbf8d&width=768&dpr=3&quality=100&sign=8aeaa7049716da68249a4bb34e5f9ca6&sv=3)

Postman screenshot of additional parameters

Both userID and ulcaApiKey can be obtained from the **My Profile** section after logging in.

[PreviousResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload)
[NextRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload)

Last updated 2 years ago

---

# Transliteration Compute Call | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call.md)
.

[Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload)
[Response Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload)

[PreviousResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload)
[NextRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload)

---

# Request Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload.md)
.

Request Payload for Individual Task[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#request-payload-for-individual-task)

----------------------------------------------------------------------------------------------------------------------------------------------------------------

ASR

Translation

TTS

Copy

    {
        "pipelineTasks": [\
            {\
                "taskType": "asr",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "xx"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                    "audioFormat": "wav",\
                    "samplingRate": 16000,\
                    "preProcessors": [\
                        "vad"\
                    ],\
                    "postProcessors": [\
                        "itn"\
                    ]\
                }\
            }\
        ],
        "inputData": {
            "input": [\
                {\
                    "source": null\
                }\
            ],
            "audio": [\
                {\
                    "audioContent": "{{generated_base64_content}}"\
                }\
            ]
        }
    }

This response contains 2 major parameters listed below and detailed further down the section:

1.  pipelineTasks
    
2.  inputData
    

### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#parameter-pipelinetasks)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes only one dictionary (line 3-13) because integrator wants to do only ASR. `**taskType**` parameter takes `String` that takes the value `**asr**`

`**config**` parameter takes a `**Dictionary**` that contains following parameters:

Language

Service ID

Audio Format

Sampling Rate

For ASR, `**language**` parameter only takes `**sourceLanguage**` which accepts [ISO-639 Series Code](https://dibd-bhashini.gitbook.io/bhashini-apis)
 of the language.

serviceId parameter is obtained from the [Pipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
 [response](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload)
 as described [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineresponseconfig)
.

`**audioFormat**` parameter accepts format of the audio which was recorded by the application.

*   For Android, `**wav**` is preferred and
    
*   For iOS, `**wav**` or `**flac**` is preferred.
    

However, the Server also accepts other well -known formats such as `**mp3**`.

Sampling Rate is determined by the application at which the audio is recorded. The Server accepts a minimum value of `**8000**` for `**samplingRate**` parameter.

Parameters other than `**taskType**`, `**serviceId**` and `**config**` are optional.

### Parameter: `inputData`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#parameter-inputdata)

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input either via `**input**` parameter or `**audio**` parameter depending on the task to be done. Since ASR is done on audio input data, for ASR,

*   `**input**` parameter is optional, of no use for ASR but
    
*   `**audio**` parameter is mandatory.
    

**audio** parameter takes `**audioContent**` parameter which accepts `**base64 String**` of the actual audio captured.

If `**audioFormat**` or/and `**samplingRate**` parameter is/are sent, integrator should make sure that these values correspond to the actual recorded audio.

Copy

    {
        "pipelineTasks": [\
            {\
                "taskType": "translation",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "hi",\
                        "targetLanguage": "en"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                    "numTranslation": "True"\
                }\
            }\
        ],
        "inputData": {
            "input": [\
                {\
                    "source": "मेरा नाम विहिर है और मैं भाषाावर्ष यूज कर रहा हूँ"\
                }\
            ],
            "audio": [\
                {\
                    "audioContent": null\
                }\
            ]
        }
    }

This response contains 2 major parameters listed below and detailed further down the section:

1.  pipelineTasks
    
2.  inputData
    

### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#parameter-pipelinetasks-1)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes only one dictionary (line 3-12) because integrator wants to do only Translation. `**taskType**` parameter takes `String` that takes the value `**translation**`

`**config**` parameter takes a `**Dictionary**` that contains following parameters:

Language

Service ID

numTranslation

For Translation, `**language**` parameter takes both `**sourceLanguage**` and `**targetLanguage**` which accepts [ISO-639 Series Code](https://bhashini.gitbook.io/bhashini-apis/)
 [](https://dibd-bhashini.gitbook.io/bhashini-apis)of the language.

serviceId parameter is obtained from the [Pipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
 [response](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload)
 as described [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineresponseconfig)
.

numTranslation is a optional parameter which enable the API to translate the numerical data/digit into the respective target language.

this feature is currently enabled only in **ai4bharat/indictrans-v2-all-gpu--t4** service Id and for devanagari script supported languages. Default value is False.

### Parameter: `inputData`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#parameter-inputdata-1)

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input either via `**input**` parameter or `**audio**` parameter depending on the task to be done. Since Transaltion is done on digital text input data, for Translation,

*   `**input**` parameter is mandatory and
    
*   `**audio**` parameter is optional and of no use for Translation.
    

**input** parameter takes `**source**` parameter which accepts `**digital text string**`.

Copy

    {
        "pipelineTasks": [       \
            {\
                "taskType": "tts",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "gu"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                    "gender": "female",\
                    "speed": 1.0, // range between 0.1 to 1.99\
                    "samplingRate": 48000               \
                }\
            }\
        ],
        "inputData": {
            "input": [\
                {\
                    "source": "મારું નામ વિહીર છે અને હું ભાષાવર્ષનો ઉપયોગ કરી રહ્યો છું"\
                }\
            ],
            "audio": [\
                {\
                    "audioContent": null\
                }\
            ]
        }
    }

This response contains 2 major parameters listed below and detailed further down the section:

1.  pipelineTasks
    
2.  inputData
    

### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#parameter-pipelinetasks-2)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes only one dictionary (line 3-12) because integrator wants to do only TTS. `**taskType**` parameter takes `String` that takes the value `**tts**`

`**config**` parameter takes a `**Dictionary**` that contains following parameters:

Language

Service ID

gender

speed

samplingRate

For TTS, `**language**` parameter only takes `**sourceLanguage**` which accepts [ISO-639 Series Code](https://dibd-bhashini.gitbook.io/bhashini-apis)
 of the language.

serviceId parameter is obtained from the [Pipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
 [response](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload)
 as described [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineresponseconfig)
.

gender parameter takes a string input which can either be:

*   male
    
*   female
    

gender parameter tells the server that integrator is requesting the generated speech in either male or female voice.

speed parameter takes a integer input which helps in controlling on how fast the synthesized voice speaks. Range between 0.1 to 1.99

*   Increased speed makes the speech sounds quicker, useful for fast-paced content like alerts or summaries.
    
*   Decreased speed makes the speech is slower and more deliberate, ideal for accessibility or language learning.
    

samplingRate parameter takes a integer value which helps in determining the number of audio samples per second in the generated speech output, measured in Hertz (Hz). It's a key parameter that affects both audio quality and file size.

### Parameter: `inputData`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#parameter-inputdata-2)

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input either via `**input**` parameter or `**audio**` parameter depending on the task to be done. Since TTS is done on digital text input data, for TTS,

*   `**input**` parameter is mandatory and
    
*   `**audio**` parameter is optional and of no use for TTS.
    

**input** parameter takes `**source**` parameter which accepts `**digital text string**`.

Request Payload for Combination of Tasks in specific sequence[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#request-payload-for-combination-of-tasks-in-specific-sequence)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ASR+Translation

Translation+TTS

ASR+Translation+TTS

Copy

    {
        "pipelineTasks": [\
            {\
                "taskType": "asr",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "xx"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                    "audioFormat": "flac",\
                    "samplingRate": 16000\
                }\
            },\
            {\
                "taskType": "translation",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "xx",\
                        "targetLanguage": "yy"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--mfkds"\
                }\
            }\
        ],
        "inputData": {
            "input": [\
                {\
                    "source": null\
                }\
            ],
            "audio": [\
                {\
                    "audioContent": "{{generated_base64_content}}"\
                }\
            ]
        }
    }

### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#parameter-pipelinetasks-3)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes two dictionaries:

*   Line 3 to 13 i.e., `**ASR Dictionary**`
    
*   Line 14 to 23 i.e., `**Translation Dictionary**`
    

because integrator wants to do `**ASR**` of the input voice followed by `**Translation**` of the digital text.

`**Line Number 7**` and `**Line Number 18**` are connected with below understanding. Consider a use-case described below:

Integrator wants to **speak** in say `**Hindi**` language and wants to **see** the **translated output** in `**Marathi**`. For this to happen, integrator has to:

*   Convert the Audio integrator has spoken to digital text i.e., ASR of Hindi
    
*   Translate this digital Hindi text to Marathi digital text i.e., Translation from Hindi to Marathi
    

Therefore, the **language code** for `**ASR**` that is to be inserted in **Line 7**, shall be `**hi**`, i.e., [ISO 639 series](https://dibd-bhashini.gitbook.io/bhashini-apis)
 code for Hindi. Once this Hindi digital text is generated, the same shall be translated to Marathi, therefore the **source language code** for `**Translation**` that is to be inserted in **Line 18**, shall also be `**hi**`, which means that **language code** in **Line 7** and **Line 18** shall be same.

For Target Language the code to be inserted in Line 19 shall be `**mr**`, i.e., [ISO 639 series](https://dibd-bhashini.gitbook.io/bhashini-apis)
 code for Marathi.

Understanding of all other parameters remains same as described above in [`**Request Payload for Individual Task**`](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#request-payload-for-individual-task)
.

Copy

    {
        "pipelineTasks": [\
            {\
                "taskType": "translation",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "hi",\
                        "targetLanguage": "yy"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--dddd"\
                }\
            },\
            {\
                "taskType": "tts",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "yy"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--csdcxsa",\
                    "gender": "female"\
                }\
            }\
        ],
        "inputData": {
            "input": [\
                {\
                    "source": "मेरा नाम विहिर है और मैं भाषाावर्ष यूज कर रहा हूँ"\
                }\
            ],
            "audio": [\
                {\
                    "audioContent": null\
                }\
            ]
        }
    }

### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#parameter-pipelinetasks-4)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes two dictionaries:

*   Line 3 to 12 i.e., `**Translation Dictionary**`
    
*   Line 13 to 22 i.e., `**TTS Dictionary**`
    

because integrator wants to do `**Translation**` of a digital text followed by `**TTS**`.

`**Line Number 8**` and `**Line Number 17**` are connected with below understanding. Consider a use-case described below:

Integrator wants to **translate** say from `**Hindi**` to `**Marathi**` language and wants to **hear** the **output** in `**Marathi**`. For this to happen, integrator has to:

*   Translate this digital Hindi text to Marathi digital text i.e., Translation from Hindi to Marathi
    
*   Generate this Marathi text speech i.e., TTS of the Marathi digital text.
    

Therefore, the **source language code** for `**Translation**` that is to be inserted in **Line 7**, shall be `**hi**`, i.e., [ISO 639 series](https://dibd-bhashini.gitbook.io/bhashini-apis)
 code for Hindi. The **target language code** to be inserted in Line 8 shall be `**mr**`, i.e., [ISO 639 series](https://dibd-bhashini.gitbook.io/bhashini-apis)
 code for Marathi.

Speech shall be generated in Marathi which means the language code to be inserted in **Line 17** shall be `**mr**`, same as **Line 8.**

Understanding of all other parameters remains same as described above in [`**Request Payload for Individual Task**`](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#request-payload-for-individual-task)
.

Copy

    {
        "pipelineTasks": [\
            {\
                "taskType": "asr",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "xx"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                    "audioFormat": "flac",\
                    "samplingRate": 16000\
                }\
            },\
            {\
                "taskType": "translation",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "xx",\
                        "targetLanguage": "yy"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--fwsd"\
                }\
            },\
            {\
                "taskType": "tts",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "yy"\
                    },\
                    "serviceId": "xxxxx--ssssss-d-ddd--fvdfg",\
                    "gender": "female"\
                }\
            }\
        ],
        "inputData": {
            "input": [\
                {\
                    "source": null\
                }\
            ],
            "audio": [\
                {\
                    "audioContent": "{{generated_base64_content}}"\
                }\
            ]
        }
    }

### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#parameter-pipelinetasks-5)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes two dictionaries:

*   Line 3 to 13 i.e., `**ASR Dictionary**`
    
*   Line 14 to 23 i.e., `**Translation Dictionary**`
    
*   Line 24 to 33 i.e., `**TTS Dictionary**`
    

because integrator wants to do `**ASR**` of the voice input, then `**Translation**` of a digital text followed by `**TTS**`.

`**Line Number 7**` and `**Line Number 18**` are connected and `**Line Number 19**` and `**Line Number 28**` with below understanding. Consider a use-case described below:

Integrator wants to **speak** in say `**Hindi**` language and wants to **hear** the **translated output** in `**Marathi**`. For this to happen, integrator has to:

*   Convert the Audio integrator has spoken to digital text i.e., ASR of Hindi
    
*   Translate this digital Hindi text to Marathi digital text i.e., Translation from Hindi to Marathi
    
*   Generate this Marathi text speech i.e., TTS of the Marathi digital text.
    

Therefore, the **language code** for `**ASR**` that is to be inserted in **Line 7**, shall be `**hi**`, i.e., [ISO 639 series](https://dibd-bhashini.gitbook.io/bhashini-apis)
 code for Hindi. Once this Hindi digital text is generated, the same shall be translated to Marathi, therefore the **source language code** for `**Translation**` that is to be inserted in **Line 18**, shall also be `**hi**`, which means that **language code** in **Line 7** and **Line 18** shall be same.

The **target language code** to be inserted in **Line 19** shall be `**mr**`, i.e., [ISO 639 series](https://dibd-bhashini.gitbook.io/bhashini-apis)
 code for Marathi.

Speech shall be generated in Marathi which means the language code to be inserted in **Line 28** shall be `**mr**`, same as **Line 19.**

Understanding of all other parameters remains same as described above in [`**Request Payload for Individual Task**`](https://bhashini.gitbook.io/bhashini-apis/)
[.](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#request-payload-for-individual-task)

Pre-Processors and Post-Processors within Compute Request[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#pre-processors-and-post-processors-within-compute-request)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ASR

Translation

TTS

In Automatic Speech Recognition (ASR) systems, preprocessors and postprocessors play a crucial role in refining the audio input and enhancing the textual output, respectively. Below, we provide details on the available preprocessors and postprocessors, along with an example of how to configure them in your request body.

**Preprocessors**

**Voice Activity Detection (VAD)**

*   **Syntax:** `"preProcessors": ["vad"]`
    
*   **Function:** VAD allows audio content longer than 30 seconds to be passed and processed. It helps identify voice activity to ensure that only the detected voice activity is processed, reducing the load and improving the efficiency of the ASR system.
    

**Denoiser**

*   **Syntax:** `"preProcessors": ["denoiser"]`
    
*   **Function:** Denoiser helps in improving the accuracy of speech recognition by reducing background noise from audio inputs.
    

**Postprocessors**

**Hotwords**

*   **Syntax:** `"postProcessors": [{"hotword_list":["`पत्रिका`"]}]`
    
*   **Function:** A hotword is postprocessor allows users to share a list of keyword or phrase in which the system is trained to recognize with higher priority or accuracy. This helps in enhancing the ASR performance. This feature is only applicable for Hindi and for service Id "bhashini/ai4bharat/conformer-multilingual-asr".
    

**Example:** a Hindi news broadcast where words like "पत्रिका" (Magazine) are frequently mentioned. Adding these as hotwords ensures they are transcribed correctly rather than being replaced by phonetically similar but incorrect words

**Inverse Text Normalization (ITN)**

*   **Syntax:** `"postProcessors": ["itn"]`
    
*   **Function:** ITN converts spoken numbers and dates into their written forms. For example, the ASR would output "two thousand and twenty three" as "2023".
    

**Punctuation**

*   **Syntax:** `"postProcessors": ["punctuation"]`
    
*   **Function:** This postprocessor adds punctuations to the ASR output, making the text more readable and closer to natural written language.
    
    **Example:**
    
    *   ASR Output: "hello how are you"
        
    *   Punctuation Output: "Hello, how are you?"
        
    

The configuration of preprocessors and postprocessors can be included within the `config` section of the request body as shown below:

Copy

    "config": {
        "language": {
            "sourceLanguage": "xx"
        },
        "serviceId": "xxxxx--ssssss-d-ddd--dddd",
        "audioFormat": "flac",
        "samplingRate": 16000,
        "preProcessors": ["vad"],
        "postProcessors": [{\
                        "hotword_list": ["पत्रिका", "रंगकर्म", "फिक्र"]\
                    }, "itn", "punctuation"]
    }

In translation (NMT) systems, postprocessors play a crucial role in refining the textual output to meet specific needs. Below, we provide details on the postprocessor available for translation, along with an example of how to configure it in your request body.

**Postprocessors**

**Glossary**

*   **Syntax:** `"postProcessors": ["glossary"]`
    
*   **Function:** The glossary postprocessor allows users to create a list of glossary terms within Bhashini Udyat under the My Profile Section once logged in. Glossary terms created are unique for each Bhashini Inference API Key generated under app names. This postprocessor ensures that specific nouns and noun phrases have their translations overridden as per the user's glossary.
    

**Example:**

*   Default Translation: "Digital India Bhashini Division" is translated to "डिजिटल इंडिया भैसिनी प्रभाग".
    
*   With Glossary Term: If the glossary term between English and Hindi is entered as "डिजिटल इंडिया भाषिणी डिवीज़न", this will override the default translation.
    

**Link to Access My Profile Page and Generate Keys and Glossary:** [Bhashini Udyat Profile Page](https://bhashini.gov.in/ulca/profile)

**Glossary Terms Usage:** Glossary terms help provide customized solutions for domain-specific translations, ensuring accuracy and context relevance in the translated output.

**Example of Glossary Usage:**

*   Case sensitivity handling (Ex: Glossary entry - English to Hindi as IPO -> आईपीओ).
    
*   Glossary entries will work by default for:
    
    1.  Entered noun/noun phrase (e.g., IPO)
        
    2.  Capitalized case (Ipo)
        
    3.  Lower case (ipo)
        
    4.  Upper case ( IPO)
        
    5.  Reverse case (if आईपीओ is the source, the target is IPO when translating from Hindi to English).
        
    

#### Configuration Example[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#configuration-example)

The configuration of the glossary postprocessor can be included within the `config` section of the request body as shown below:

Copy

    "config": {
        "language": {
            "sourceLanguage": "hi",
            "targetLanguage": "xx"
        },
        "postProcessors": ["glossary"]
        "serviceId": "xxxxx--ssssss-d-ddd--dddd"
    }

In Text to Speech (TTS) systems, preprocessor, postprocessors play a crucial role in refining the audio output and enhancing the audio quality respectively. Below, we have provide details on the available preprocessor, postprocessors, along with an format of how to configure them in your request body.

**Preprocessors**

**Text Normalization (TN)**

*   **Syntax:** `"preProcessors": ["text-normalization"]`
    
*   **Function:** It converts numbers and dates into their name forms. For example, the TTS would output "2025" as "two thousand twenty five".
    

**Postprocessors**

**High Compression**

*   **Syntax:** `"postProcessors": ["high-compression"]`
    
*   **Function:** This helps minimize audio file size during download without compromising quality, making it suitable for low-bandwidth(network) environment and applications where storage is a primary concern It also speeds up transmission and playback by reducing latency. It gives 64kbps audio.
    

**Low Compression**

*   **Syntax:** `"postProcessors": ["low-compression"]`
    
*   **Function:** This helps minimize audio file size during download without a significant loss in audio quality, making it suitable for low-bandwidth(network) environments. It also speeds up transmission and playback by reducing latency. It gives 128kbps audio.
    

[PreviousPipeline Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call)
[NextResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload)

Last updated 1 year ago

---

# Response Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload.md)
.

Request sent without configuration parameter

Request sent with Configuration Parameter

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#complete-payload)

--------------------------------------------------------------------------------------------------------------------------

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#complete-payload-1)

Copy

    {
        "languages": [\
            {\
                "sourceLanguage": "bn",\
                "targetLanguageList": [\
                    "en",\
                    "as",\
                    "gu",\
                    "hi"              \
                ]\
            },\
            {\
                "sourceLanguage": "en",\
                "targetLanguageList": [               \
                    "ml",\
                    "mr",\
                    "or",\
                    "pa",\
                    "ta",\
                    "te"\
                ]\
            },       \
            {\
                "sourceLanguage": "hi",\
                "targetLanguageList": [\
                    "en",\
                    "as",\
                    "bn",\
                    "gu",\
                    "kn"\
                ]\
            }\
        ],
        "pipelineResponseConfig": [\
            {\
                "taskType": "asr",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",\
                        "modelId": "6411746956e9de23f65b5426",\
                        "language": {\
                            "sourceLanguage": "bn"\
                        },\
                        "domain": [\
                            "general"\
                        ]\
                    },\
                    {\
                        "serviceId": "ai4bharat/conformer-en-gpu--t4",\
                        "modelId": "63ee09c3b95268521c70cd7c",\
                        "language": {\
                            "sourceLanguage": "en"\
                        },\
                        "domain": [\
                            "general"\
                        ]\
                    },\
                    {\
                        "serviceId": "ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",\
                        "modelId": "64117455b1463435d2fbaec4",\
                        "language": {\
                            "sourceLanguage": "hi"\
                        },\
                        "domain": [\
                            "general"\
                        ]\
                    }\
                ]\
            },\
            {\
                "taskType": "tts",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/indic-tts-coqui-misc-gpu--t4",\
                        "modelId": "63f7384c2ff3ab138f88c64e",\
                        "language": {\
                            "sourceLanguage": "en"\
                        },\
                        "supportedVoices": [\
                            "male",\
                            "female"\
                        ]\
                    },\
                    {\
                        "serviceId": "ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",\
                        "modelId": "6348db0bfd966563f61bc2c0",\
                        "language": {\
                            "sourceLanguage": "as"\
                        },\
                        "supportedVoices": [\
                            "male",\
                            "female"\
                        ]\
                    }\
                ]\
            },\
            {\
                "taskType": "translation",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/indictrans-fairseq-i2e-gpu--t4",\
                        "modelId": "6110f7bc014fa35d5e767c3b",\
                        "language": {\
                            "sourceLanguage": "bn",\
                            "targetLanguage": "en"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indictrans-fairseq-i2i-gpu--t4",\
                        "modelId": "6214b148751fc8007d24084c",\
                        "language": {\
                            "sourceLanguage": "bn",\
                            "targetLanguage": "as"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indictrans-fairseq-e2i-gpu--t4",\
                        "modelId": "6110f7ce014fa35d5e767c3c",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "as"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indictrans-fairseq-e2i-gpu--t4",\
                        "modelId": "6110f7da014fa35d5e767c3d",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "bn"\
                        }\
                    }\
                ]\
            }\
        ],
        "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
            "inferenceApiKey": {
                "name": "Authorization",
                "value": "cZVqccgm-LTAzxQVp6jjznmSR5RgKM"
            },
            "isMultilingualEnabled": true,
            "isSyncApi": true
        }
    }

Complete Payload shows the JSON structure of the content that is received when Integrator makes a ULCA Config Call without any configuration details as detailed in `Tab 1` of [**Request Payload**](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)

**Note: The above payload is used for reference. Response may differ based on the pipeline used by the integrator.** This response contains 3 major parameters listed below and detailed further down the section:

1.  [languages](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-languages)
    
2.  [pipelineResponseConfig](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineresponseconfig)
    
3.  [pipelineInferenceAPIEndPoint](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)
    

### Parameter: `languages`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-languages)

This parameter helps integrator to know what languages are available that can be used for the requested pipeline tasks in that sequence. For example, consider scenarios where Integrator requests for either:

*   Individual Task i.e., either ASR or Translation or TTS as shown [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#integrators-want-to-do-individual-tasks)
    
*   Combination of Tasks in that sequence i.e.,
    
    *   ASR+Translation or
        
    *   Translation+TTS or
        
    *   ASR+Translation+TTS as shown [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#integrators-want-to-do-combination-of-tasks-in-that-order)
        
    

For Single Tasks, the understanding is straight-forward that the languages appearing in the response corresponds to that task. e.g.

*   If the integrator wants to do `**only ASR**`, the languages appearing shows that Server can do ASR in these languages. In this case, parameters `**sourceLanguage**` and `**targetLanguageList**` will contain the same value since for ASR involves only one language unlike Translation where source and target (two) languages are involved. In this case, `**targetLanguageList**` can safely be ignored and only `**sourceLanguage**` can be used.
    
*   If the integrator wants to do `**only TTS**`, the languages appearing shows that Server can do TTS in these languages. In this case, parameters `**sourceLanguage**` and `**targetLanguageList**` will contain the same value since for TTS too only one language is involved. In this case too, `**targetLanguageList**` can safely be ignored and only `**sourceLanguage**` can be used.
    

Usual format of language for such cases is below:

Supported Languages for requested Pipeline.[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#supported-languages-for-requested-pipeline)

Copy

    "languages": [\
            {\
                "sourceLanguage": "bn",\
                "targetLanguageList": [\
                    "bn"              \
                ]\
            },\
            {\
                "sourceLanguage": "en",\
                "targetLanguageList": [               \
                    "en"\
                ]\
            },       \
            {\
                "sourceLanguage": "hi",\
                "targetLanguageList": [\
                    "hi"\
                ]\
            }\
        ]

*   If the integrator wants to do `**only Translation**`, the languages appearing shows that Server can do Translation in these languages. In this case, parameters `**sourceLanguage**` and `**targetLanguageList**` means that for the languages appearing in `**targetLanguageList**` are the ones in which Server can do translation FROM the language that appear in `**sourceLanguage**`.
    

For Combination of Tasks, the understanding is that the languages appearing in the response are the ones which Server can cater to, for the complete task sequence sent by the integrator. e.g.

*   If the integrator wants to do `**ASR and Translation**` together in that sequence, the languages appearing shows that the Server can do this combination in that sequence for these languages. In this case, the Server would be able to do this combination for the languages appearing in `**targetLanguageList**`, if the input is given in the language mentioned in `**sourceLanguage**` parameter.
    
*   If the integrator wants to do `**Translation and TTS**` together in that sequence, the languages appearing shows that the Server can do this combination in that sequence for these languages. In this case, the Server would be able to do this combination for the languages appearing in `**targetLanguageList**`, if the input is given in the language mentioned in `**sourceLanguage**` parameter.
    
*   If the integrator wants to do `**ASR, then Translation and then TTS**` together in that sequence, the languages appearing shows that the Server can do this combination in that sequence for these languages. In this case, the Server would be able to do this combination for the languages appearing in `**targetLanguageList**`, if the input is given in the language mentioned in `**sourceLanguage**` parameter.
    

Usual format of language for such cases is below:

Supported Languages for requested Pipeline.[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#supported-languages-for-requested-pipeline-1)

Copy

    "languages": [\
            {\
                "sourceLanguage": "bn",\
                "targetLanguageList": [\
                    "en",\
                    "as",\
                    "gu",\
                    "hi"              \
                ]\
            },\
            {\
                "sourceLanguage": "en",\
                "targetLanguageList": [               \
                    "ml",\
                    "mr",\
                    "or",\
                    "pa",\
                    "ta",\
                    "te"\
                ]\
            },       \
            {\
                "sourceLanguage": "hi",\
                "targetLanguageList": [\
                    "en",\
                    "as",\
                    "bn",\
                    "gu",\
                    "kn"\
                ]\
            }\
        ]

### Parameter: `pipelineResponseConfig`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineresponseconfig)

This parameter helps the integrator to obtain the `**Service ID**` for a particular task type and language(s) associated with that task.

The task types appearing here will be the same as the ones that the integrator requested while sending the `**pipelineTasks**` parameter in [Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)
 e.g., Integrator request for configuration of the combination of ASR, Translation and TTS together, the `**pipelineResponseConfig**` parameter in the output will contain the JSON data as shown below. It will contain three dictionaries for each task type ASR, Translation and TTS. If Integrator requested for a combination of ASR and Translation, this parameter would contain JSON data for ASR and Translation only. Now consider, Integrator knows the language for which the combination ASR, Translation and TTS is to be performed (language may be determined by asking the end-user etc.). Say the language pair chosen is `**Bengali**` to `**Assamese**`. Integrator shall now obtain the Service ID correspondingly in the below manner:

1.  Obtain Service ID for doing `**ASR**` in `**Bengali**`. Line 6 from Dictionary of Line 5-14 below.
    
2.  Obtain Service ID for doing `**Translation**` from `**Bengali**` to `**Assamese**`. Line 49 from Dictionary of Line 48-55 below.
    
3.  Obtain Service ID for doing `**TTS**` in `**Assamese**`. Line 89 from Dictionary of Line 88-98 below.
    

These Service IDs will be used in the [Pipeline Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call)
.

For each `**taskType**` in the response, there may appear additional configuration parameters that are specific to each `**taskType**`. e.g.,

*   As seen below, for `**taskType ASR**`, `**domain**` parameter appears which helps integrator to understand the domain(s) (general, agriculture, medical etc.), this particular Service ID is capable of providing output for.
    
*   Similarly, for `**taskType TTS**`, `**supportedVoice**` parameter appears which helps integrator to understand which all voices are available for a particular language that is serviced by that specific Service ID.
    

Configuration Details and Service IDs for requested pipeline tasks.[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#configuration-details-and-service-ids-for-requested-pipeline-tasks)

Copy

    "pipelineResponseConfig": [\
            {\
                "taskType": "asr",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",\
                        "modelId": "6411746956e9de23f65b5426",\
                        "language": {\
                            "sourceLanguage": "bn"\
                        },\
                        "domain": [\
                            "general"\
                        ]\
                    },\
                    {\
                        "serviceId": "ai4bharat/conformer-en-gpu--t4",\
                        "modelId": "63ee09c3b95268521c70cd7c",\
                        "language": {\
                            "sourceLanguage": "en"\
                        },\
                        "domain": [\
                            "general"\
                        ]\
                    },\
                    {\
                        "serviceId": "ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",\
                        "modelId": "64117455b1463435d2fbaec4",\
                        "language": {\
                            "sourceLanguage": "hi"\
                        },\
                        "domain": [\
                            "general"\
                        ]\
                    }\
                ]\
            },\
            {\
                "taskType": "translation",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/indictrans-fairseq-i2e-gpu--t4",\
                        "modelId": "6110f7bc014fa35d5e767c3b",\
                        "language": {\
                            "sourceLanguage": "bn",\
                            "targetLanguage": "en"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indictrans-fairseq-i2i-gpu--t4",\
                        "modelId": "6214b148751fc8007d24084c",\
                        "language": {\
                            "sourceLanguage": "bn",\
                            "targetLanguage": "as"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indictrans-fairseq-e2i-gpu--t4",\
                        "modelId": "6110f7ce014fa35d5e767c3c",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "as"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indictrans-fairseq-e2i-gpu--t4",\
                        "modelId": "6110f7da014fa35d5e767c3d",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "bn"\
                        }\
                    }\
                ]\
            },\
            {\
                "taskType": "tts",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/indic-tts-coqui-misc-gpu--t4",\
                        "modelId": "63f7384c2ff3ab138f88c64e",\
                        "language": {\
                            "sourceLanguage": "en"\
                        },\
                        "supportedVoices": [\
                            "male",\
                            "female"\
                        ]\
                    },\
                    {\
                        "serviceId": "ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",\
                        "modelId": "6348db0bfd966563f61bc2c0",\
                        "language": {\
                            "sourceLanguage": "as"\
                        },\
                        "supportedVoices": [\
                            "male",\
                            "female"\
                        ]\
                    }\
                ]\
            }\
        ]

### Parameter: `pipelineInferenceAPIEndPoint`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)

This parameter helps the integrator to know the details of the [Pipeline Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call)
 where to send (`**callbackURL**` parameter) and shall be sent along with the `**Authorization Key-Value pair**` received under `**inferenceApiKey**` parameter which will be used for authentication of the same.

**Note: The above sample config call is used for reference. Response may differ based on the pipeline used by the integrator.**

Details for Actual Inferencing.[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#details-for-actual-inferencing)

Copy

    "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
            "inferenceApiKey": {
                "name": "Authorization",
                "value": "cZVqccgm-LTAzxQVp6jjznmSR5RgKM"
            },
            "isMultilingualEnabled": true,
            "isSyncApi": true
        }

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#complete-payload-2)

----------------------------------------------------------------------------------------------------------------------------

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#complete-payload-3)

Copy

    {
        "languages": [\
            {\
                "sourceLanguage": "gu",\
                "targetLanguageList": [\
                    "bn"\
                ]\
            }\
        ],
        "pipelineResponseConfig": [\
            {\
                "taskType": "asr",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/conformer-multilingual-indo_aryan-gpu--t4",\
                        "modelId": "6411746056e9de23f65b5425",\
                        "language": {\
                            "sourceLanguage": "gu"\
                        },\
                        "domain": [\
                            "general"\
                        ]\
                    }\
                ]\
            },\
            {\
                "taskType": "translation",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/indictrans-fairseq-i2i-gpu--t4",\
                        "modelId": "62023eeb3fc51c3fe32b8c5b",\
                        "language": {\
                            "sourceLanguage": "gu",\
                            "targetLanguage": "bn"\
                        }\
                    }\
                ]\
            },\
            {\
                "taskType": "tts",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/indic-tts-coqui-indo_aryan-gpu--t4",\
                        "modelId": "636e60e586369150cb00432a",\
                        "language": {\
                            "sourceLanguage": "bn"\
                        },\
                        "supportedVoices": [\
                            "male",\
                            "female"\
                        ]\
                    }\
                ]\
            }\
        ],
        "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
            "inferenceApiKey": {
                "name": "Authorization",
                "value": "m-LTAzxQVp6jjznmSR5RgKM"
            },
            "isMultilingualEnabled": true,
            "isSyncApi": true
        }
    }

Complete Payload shows the JSON structure of the content that is received when Integrator makes a ULCA Config Call with some configuration details as detailed in `Tab 2` of [Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)
. Here, the integrator has requested to do a combination of tasks ASR, Translation and TTS in that sequence from `**Gujarati**` to `**Bengali**`

### Parameter: `languages`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-languages-1)

The understanding of the parameters remains same as in previous tab. Since the languages were already known to the integrator before-hand, therefore, the response contains configuration details for those languages only.

There may occur a possibility that Integrator wants to do any individual task or combination of tasks in a sequence for the languages that are `**not**` supported by that `**pipeline ID**` in which case the following response will be obtained: **Response Code: 400 Bad Request Response Body:**

Copy

    {
        "code": "400 BAD_REQUEST",
        "message": "Sequence of languages not supported",
        "timestamp": "2023-04-14T06:32:12.133+00:00"
    }

In such cases, it is recommended to send Pipeline Config Request without Configuration as shown in `Tab 1` under [Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)
 Using which Integrators will know what all languages are supported by that pipeline ID.

### Parameter: `pipelineResponseConfig`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineresponseconfig-1)

The understanding of the parameters remains same as in previous tab. Since the languages were already known to the integrator before-hand, therefore, the response contains configuration details for those languages only.

### Parameter: `pipelineInferenceAPIEndPoint`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint-1)

The understanding of the parameters remains same as in previous tab.

[PreviousRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)
[NextPipeline Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call)

Last updated 2 years ago

---

# Response Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload.md)
.

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#complete-payload)

---------------------------------------------------------------------------------------------------------------------------

ASR+Translate+TTS[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#asrtranslatetts)

Copy

    {
        "pipelineResponse": [\
            {\
                "taskType": "asr",\
                "config": {\
                    "serviceId": "ai4bharat/conformer-hi-gpu--t4",\
                    "language": {\
                        "sourceLanguage": "hi",\
                        "sourceScriptCode": ""\
                    },\
                    "audioFormat": "flac",\
                    "encoding": null,\
                    "samplingRate": 16000,\
                    "postProcessors": null\
                },\
                "output": [\
                    {\
                        "source": "मेरा नाम महीर है और मैं भाषा यूज़ कर रहा हूँ"\
                    }\
                ],\
                "audio": null\
            },\
            {\
                "taskType": "translation",\
                "config": null,\
                "output": [\
                    {\
                        "source": "मेरा नाम महीर है और मैं भाषा यूज़ कर रहा हूँ",\
                        "target": "माझे नाव माहिर आहे आणि मी भाषेच वापरत आहे"\
                    }\
                ],\
                "audio": null\
            },\
            {\
                "taskType": "tts",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "mr",\
                        "sourceScriptCode": ""\
                    },\
                    "audioFormat": "wav",\
                    "encoding": "base64",\
                    "samplingRate": 22050,\
                    "postProcessors": null\
                },\
                "output": null,\
                "audio": [\
                    {\
                        "audioContent": "{{returned_base64_content}}",\
                        "audioUri": null\
                    }\
                ]\
            }\
        ]
    }

The above JSON Response shows the output of the combination of ASR, Translation and TTS task requested by the integrator in that order. Below we will discuss the individual task response as well as combination of tasks in specific sequence.

Response for Payload sent for Individual Task Request[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#response-for-payload-sent-for-individual-task-request)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ASR

Translation

TTS

Copy

    {
        "taskType": "asr",
        "config": {
            "serviceId": "xxxxx--ssssss-d-ddd--dddd",
            "language": {
                "sourceLanguage": "hi",
                "sourceScriptCode": ""
            },
            "audioFormat": "flac",
            "encoding": null,
            "samplingRate": 16000,
            "postProcessors": null
        },
        "output": [\
            {\
                "source": "मेरा नाम महीर है और मैं भाषा यूज़ कर रहा हूँ"\
            }\
        ],
        "audio": null
    }

For `**individual ASR task request**` sent by the integrator, the response will contain only one dictionary where `**taskType**` will be `**asr**`.

### Parameter: `config`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#parameter-config)

`**config**` parameter returns the configuration details of the output generated.

### Parameter: `output`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#parameter-output)

`**output**` parameter

contains

`**source**` parameter which gives the actual digital text of the audio sent as a part of the request as detailed [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload)
.

Copy

    {
        "taskType": "translation",
        "config": null,
        "output": [\
            {\
                "source": "मेरा नाम महीर है और मैं भाषा यूज़ कर रहा हूँ",\
                "target": "My name is Vihar and I am using BhashaVarsh."\
            }\
        ],
        "audio": null
    }

For `**individual Translation task request**` sent by the integrator, the response will contain only one dictionary where `**taskType**` will be `**translation**`.

### Parameter: `config`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#parameter-config-1)

`**config**` parameter returns the configuration details of the output generated.

### Parameter: `output`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#parameter-output-1)

`**output**` parameter

contains

`**source**` parameter which shows the digital text which was sent as an input as a part of the request.

`**source**` parameter which gives the actual digital text of the audio sent as a part of the request as detailed [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#translation)
[.](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload#translation)

Copy

    {
        "taskType": "tts",
        "config": {
            "language": {
                "sourceLanguage": "mr",
                "sourceScriptCode": ""
            },
            "audioFormat": "wav",
            "encoding": "base64",
            "samplingRate": 22050,
            "postProcessors": null
        },
        "output": null,
        "audio": [\
            {\
                "audioContent": "{{returned_base64_content}}",\
                "audioUri": null\
            }\
        ]
    }

For `**individual TTS task request**` sent by the integrator, the response will contain only one dictionary where `**taskType**` will be `**tts**`.

### Parameter: `config`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#parameter-config-2)

`**config**` parameter returns the configuration details of the output generated.

### Parameter: `audio`[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#parameter-audio)

`**audio**` parameter

contains

`**audioContent**` parameter which gives the `**base64 encoded content**` of the audio content generated on the server and returned. The same shall be converted for a `**wav**` file which can then be heard by the integrator.

Response for Payload sent for Individual Task Request[](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#response-for-payload-sent-for-individual-task-request-1)

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ASR+Translation

Translation+TTS

ASR+Translation+TTS

Output of `**ASR+Translation**` comes in the form of combination of `**ASR**` and `**Translation**` dictionary as detailed [above](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#response-for-payload-sent-for-individual-task-request)
.

Copy

    {
        "pipelineResponse": [\
            {\
                "taskType": "asr",\
                "config": {\
                    "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                    "language": {\
                        "sourceLanguage": "hi",\
                        "sourceScriptCode": ""\
                    },\
                    "audioFormat": "flac",\
                    "encoding": null,\
                    "samplingRate": 16000,\
                    "postProcessors": null\
                },\
                "output": [\
                    {\
                        "source": "मेरा नाम महीर है और मैं भाषावर्ष यूज़ कर रहा हूँ"\
                    }\
                ],\
                "audio": null\
            },\
            {\
                "taskType": "translation",\
                "config": null,\
                "output": [\
                    {\
                        "source": "मेरा नाम महीर है और मैं भाषावर्ष यूज़ कर रहा हूँ",\
                        "target": "माझे नाव माहिर आहे आणि मी भाषेचे वर्ष वापरत आहे"\
                    }\
                ],\
                "audio": null\
            }\
        ]
    }

Output of `**Translation+TTS**` comes in the form of combination of `**Translation**` and `**TTS**` dictionary as detailed [above](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#response-for-payload-sent-for-individual-task-request)
.

Copy

    {
        "pipelineResponse": [\
            {\
                "taskType": "translation",\
                "config": null,\
                "output": [\
                    {\
                        "source": "मेरा नाम महीर है और मैं भाषावर्ष यूज़ कर रहा हूँ",\
                        "target": "माझं नाव माहिर आहे आणि मी भाषेचे वर्ष वापरत आहे."\
                    }\
                ],\
                "audio": null\
            },\
            {\
                "taskType": "tts",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "mr",\
                        "sourceScriptCode": ""\
                    },\
                    "audioFormat": "wav",\
                    "encoding": "base64",\
                    "samplingRate": 22050,\
                    "postProcessors": null\
                },\
                "output": null,\
                "audio": [\
                    {\
                        "audioContent": "{{generated_base64_content}}",\
                        "audioUri": null\
                    }\
                ]\
            }\
        ]
    }

Output of ASR+Translation+TTS comes in the form of combination of `**ASR**`, `**Translation**` and `**TTS**` dictionary as detailed [above](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload#response-for-payload-sent-for-individual-task-request)
.

Copy

    {
        "pipelineResponse": [\
            {\
                "taskType": "asr",\
                "config": {\
                    "serviceId": "ai4bharat/conformer-hi-gpu--t4",\
                    "language": {\
                        "sourceLanguage": "hi",\
                        "sourceScriptCode": ""\
                    },\
                    "audioFormat": "flac",\
                    "encoding": null,\
                    "samplingRate": 16000,\
                    "postProcessors": null\
                },\
                "output": [\
                    {\
                        "source": "मेरा नाम महीर है और मैं भाषा वर्ष यूज़ कर रहा हूँ"\
                    }\
                ],\
                "audio": null\
            },\
            {\
                "taskType": "translation",\
                "config": null,\
                "output": [\
                    {\
                        "source": "मेरा नाम महीर है और मैं भाषा वर्ष यूज़ कर रहा हूँ",\
                        "target": "माझे नाव माहिर आहे आणि मी भाषेचे वर्ष वापरत आहे"\
                    }\
                ],\
                "audio": null\
            },\
            {\
                "taskType": "tts",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "mr",\
                        "sourceScriptCode": ""\
                    },\
                    "audioFormat": "wav",\
                    "encoding": "base64",\
                    "samplingRate": 22050,\
                    "postProcessors": null\
                },\
                "output": null,\
                "audio": [\
                    {\
                        "audioContent": "{{generated_base64_content}}",\
                        "audioUri": null\
                    }\
                ]\
            }\
        ]
    }

[PreviousRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload)
[NextTransliteration Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call)

Last updated 1 year ago

---

# Request Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/request-payload.md)
.

Optical Character Recognition

Copy

    {
        "pipelineTasks": [\
            {\
                "taskType": "ocr",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "ta"\
                    },\
                    "serviceId": "{{ocr_service_id}}",\
                    "textDetection":"False"\
                }\
            }\
        ],
        "inputData": {
            "image": [\
                {\
                "imageUri": "INSERT_IMAGE_URL_HERE"\
                "imageContent": "INSERT_BASE64_IMAGECONTENT_HERE"\
                 \
                }\
            ]
        }
    }

This request contains 2 major parameters listed below and detailed further down the section:

1.  pipelineTasks
    
2.  inputData
    

#### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/request-payload#parameter-pipelinetasks)

**Type:** Array

This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes only one dictionary (line 2-9) because integrator wants to do only Audio language detection. `**taskType**` parameter takes `String` that takes the value **ocr**

`**config**` is a single key parameter which maps to another object called **serviceId**

`**sourceLanguage**` is a key parameter which defines the output language in which the texts displays

`**textDetection**`is a key parameter which decides whether to enable or disable the inbuilt preprocessor (word-detector). it is of a Boolean value. this parameter should be sent in request body when the service ID is bhashini/iiith-bhasha-ocr.

in other 2 cases, pre processor should be sent as word detector to retrieve a clear output text content.

Service Id

serviceId parameter identifies the specific service/trained model you want to use.

The **bhashini/iiith-bhasha-ocr** serviceId is used for printed text images.

For serviceId as "**bhashini/iiith-bhasha-ocr**", below are the supported languages-

• Assamese

• Bengali

• English

• Gujarati

• Hindi

• Kannada

• Malayalam

• Manipuri

• Marathi

• Oriya

• Punjabi

• Tamil

• Telugu

The **bhashini/iiith-ocr-sceneText-all** serviceId is used for scene text images.

For serviceId as "**bhashini/iiith-ocr-sceneText-all**", below are the supported languages-

• Assamese

• Bengali

• Gujarati

• Hindi

• Kannada

• Malayalam

• Manipuri

• Marathi

• Oriya

• Punjabi

• Tamil

• Telugu

• Urdu

The **bhashini/iiith-ocr-hw-all** serviceId is used for hand written images.

For serviceId as "**bhashini/iiith-ocr-hw-all**", below are the supported languages-

• Assamese

• Bengali

• English

• Gujarati

• Hindi

• Kannada

• Malayalam

• Manipuri

• Marathi

• Oriya

• Punjabi

• Tamil

• Telugu

• Urdu

#### Parameter: `inputData`[](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/request-payload#parameter-inputdata)

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. in this case, the input is taken via imageUri or imageContent (base64 format).

either user can pass **imageUri** as input or **imageContent** as input.

[PreviousOCR Modalities Overview](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/ocr-modalities-overview)
[NextResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/response-payload)

Last updated 1 year ago

---

# Optical Character Recognition Call | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call.md)
.

**Endpoint:** [**https://dhruva-api.bhashini.gov.in/services/inference/pipeline**](https://dhruva-api.bhashini.gov.in/services/inference/pipeline)

**Additional Headers:**

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.

*   Accept: \*/\*
    
*   Authorization: INSERT\_API\_KEY\_HERE
    
*   Content-Type: application/json
    

Authorization : it is a HTTP header which is used to authenticate the user and permission of the requester to use protected resources. Authorization key value can be obtained from the My Profile section under the App name -> inference API key value after logging in to Bhashini-Udyat.

Accept : it is a HTTP header which is used to specify the types of content they can process. This helps the server understand what kind of response to send back.

Content-Type : it is HTTP header which is used to indicate the media type of the resource being sent. This helps the user understand how to process the content.

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, **Authorization, Accept** and **Content-Type** are the additional parameters sent.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Fuploads%252F9GuKNajN8uWpPAI9uvEZ%252Fimage.png%3Falt%3Dmedia%26token%3Dfcdf1bdd-9c0a-489e-b2f4-c764592f6ec6&width=768&dpr=3&quality=100&sign=9498814901a430d5d5a9e1d0fbfd65b9&sv=3)

[PreviousResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload)
[NextOCR Modalities Overview](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/ocr-modalities-overview)

Last updated 1 year ago

---

# Request Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload.md)
.

Without configuration parameters

With Configuration Parameters

Copy

    {
        "pipelineTasks" : [\
            \
            {\
                "taskType": "transliteration"\
            }\
            \
        ],
        "pipelineRequestConfig" : {
            "pipelineId" : "xxxx8d51ae52cxxxxxxxx"
        }
    }

### Parameters[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#parameters)

We will now understand about each parameter available as a part of this payload. **taskType**

**Type:** String

*   Line 4-6 for Transliteration
    

#### pipelineTasks[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#pipelinetasks)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` as defined above, that are to be done by the integrator. The sequence of tasks matter. In the above example, the configuration that will be returned back in the response will be for tasks ASR, Translation and TTS in that order. Each `pipelineId` (discussed below), may support few individual or task sequences as explained [here](https://dibd-bhashini.gitbook.io/bhashini-apis)
 and [here](https://dibd-bhashini.gitbook.io/bhashini-apis)
 and detailed out below.

#### pipelineId[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#pipelineid)

**Type:** String `pipelineId` takes a string value of the specific pipeline integrator wants to use. The pipeline ID can be obtained either via Pipeline Search Call or via ULCA Web based on the description which helps the integrator to understand what a pipeline can or cannot do. Each pipeline ID may support multiple task and task sequences.

The same has been explained [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call)
 and [here](https://dibd-bhashini.gitbook.io/bhashini-apis)
.

#### pipelineRequestConfig[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#pipelinerequestconfig)

**Type:** Dictionary This parameter takes in the configuration requested to do the sequence of tasks defined under parameter [pipelineTasks](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#pipelinetasks)
.

### [](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#undefined-1)

Copy

    {
        "pipelineTasks": [\
            {\
                "taskType": "transliteration",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "en"\
                    }\
                }\
            }\
            \
        ],
        "pipelineRequestConfig": {
            "pipelineId" : "xxxx8d51ae52cxxxxxxxx"
        }
    }

### Parameters[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#parameters-1)

Only additional parameter `config` is detailed out below. Rest of the parameters' understanding remains the same as [Without configuration parameters](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#without-configuration-parameters)
.

#### config[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#config)

**Type:** dictionary `config` parameter is used for sending configuration parameters to the server for each `taskType`. Each `taskType` may have some common parameters such as `language` and some parameters which are specific to each `taskType`.

Currently, there are no additional `taskType` specific parameters. Once added, they will be described here.

#### config[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#config-1)

Transliteration

**Type:** dictionary

contains: **language Type:** dictionary contains: **sourceLanguage Type:** String Source Language will take the [ISO-639 code](https://bhashini.gitbook.io/bhashini-apis/)
 of the language as the input. This parameter will tell the server that integrator wants to receive the information and details about Speech Recognition in this specific language.

[PreviousTransliteration Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call)
[NextResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload)

Last updated 1 year ago

---

# Text Language Detection Compute Call | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call.md)
.

**Endpoint:** [**https://dhruva-api.bhashini.gov.in/services/inference/pipeline**](https://dhruva-api.bhashini.gov.in/services/inference/pipeline)

**Additional Headers:**

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.

*   Accept: \*/\*
    
*   Authorization: INSERT\_API\_KEY\_HERE
    
*   Content-Type: application/json
    

Authorization : it is a HTTP header which is used to authenticate the user and permission of the requester to use protected resources. Authorization key value can be obtained from the My Profile section under the App name -> inference API key value after logging in to Bhashini-Udyat.

Accept : it is a HTTP header which is used to specify the types of content they can process. This helps the server understand what kind of response to send back.

Content-Type : it is HTTP header which is used to indicate the media type of the resource being sent. This helps the user understand how to process the content.

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, **Authorization, Accept** and **Content-Type** are the additional parameters sent.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Fuploads%252FJ4c9DFEpDwyc3PWE8ZIZ%252Fimage.png%3Falt%3Dmedia%26token%3D07f55e8e-113e-44d2-939d-375581541124&width=768&dpr=3&quality=100&sign=eb8ed611811c59e5bd3983ac44ac4e7e&sv=3)

[PreviousResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/response-payload)
[NextRequest payload](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/request-payload)

Last updated 1 year ago

---

# Request payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/request-payload.md)
.

Text Language Detection payload

Copy

    {
        "pipelineTasks": [\
            {\
                "taskType": "txt-lang-detection",\
                "config": {\
                    "serviceId": "{{tld_service_id}}"\
                }\
            }\
        ],
        "inputData": {
            "input": [\
                {\
                    "source": "INSERT_TEXT_HERE"\
                }\
            ]
        }
    }
    

This request contains 2 major parameters listed below and detailed further down the section:

1.  pipelineTasks
    
2.  inputData
    

### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/request-payload#parameter-pipelinetasks)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes only one dictionary (line 2-9) because integrator wants to do only text language detection. `**taskType**` parameter takes `String` that takes the value **txt-lang-detection**

`**config**` is a single key parameter which maps to another object called serviceId.

Service ID

serviceId parameter identifies the specific service/trained model you want to use.

For serviceId as "**bhashini/indic-lang-detection-all**", below are the supported languages-

• Assamese

• Bengali

• Bodo

• Dogri

• English

• Gujarati

• Hindi

• Kannada

• Kashmiri

• Konkani

• Maithili

• Malayalam

• Manipuri

• Marathi

• Nepali

• Oriya

• Punjabi

• Sanskrit

• Santali

• Sindhi

• Tamil

• Telugu

• Urdu

For serviceId as "**bhashini/iiiith/indic-lang-detection-all**", below are the supported languages-

• Assamese

• Bengali

• English

• Gujarati

• Hindi

• Kannada

• Malayalam

• Manipuri

• Marathi

• Oriya

• Punjabi

• Tamil

• Telugu

• Urdu

### Parameter: `inputData`[](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/request-payload#parameter-inputdata)

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input via **source** parameter .

input text content can be added as a value for **source** paramater under **inputData** complex tag

[PreviousText Language Detection Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call)
[NextResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/response-payload)

Last updated 1 year ago

---

# Request Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload.md)
.

Request Payload for Transliteration Task[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload#request-payload-for-transliteration-task)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Transliteration

Copy

    
    {
        "pipelineTasks": [\
            {\
                "taskType": "transliteration",\
                "config": {\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "hi"\
                    },\
                    "serviceId": "{{trans_service_id}}",\
                    "isSentence": false,\
                    "numSuggestions": 7\
                }\
            }\
        ],
        "inputData": {
            "input": [\
                {\
                    "source": "ki"\
                }\
            ]
        }
    }
    

This response contains 2 major parameters listed below and detailed further down the section:

1.  pipelineTasks
    
2.  inputData
    

### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload#parameter-pipelinetasks)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes only one dictionary (line 3-13) because integrator wants to do only ASR. `**taskType**` parameter takes `String` that takes the value `**asr**`

`**config**` parameter takes a `**Dictionary**` that contains following parameters:

Language

Service ID

isSentence

numSuggestions

For ASR, `**language**` parameter only takes `**sourceLanguage**` which accepts [ISO-639 Series Code](https://dibd-bhashini.gitbook.io/bhashini-apis)
 of the language.

serviceId parameter is obtained from the [Transliteration Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call)
 [response](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload)
 as described [here](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload)
.

isSentence set to true and false for getting response in sentence.

In the given request, the "numSuggestions" parameter is used in the "transliteration" task configuration. It is used to specify the number of transliteration suggestions that the task should provide.

Parameters other than `**taskType**`, `**serviceId**` and `**config**` are optional.

### Parameter: `inputData`[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload#parameter-inputdata)

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input either via `**input**` parameter .

*   `**input**` parameter takes the text in source key
    

[PreviousTransliteration Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call)
[NextResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload)

Last updated 1 year ago

---

# Download Postman Collection | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/download-postman-collection.md)
.

Create Workspace and import Collection

In Postman, access the `**Workspaces**` drop-down menu and click on `**Create Workspace**`

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252F61Q9H3hRUXKcXEHCG29R%252Fimage.png%3Falt%3Dmedia%26token%3D17422622-fb70-49cf-9397-0b74e2c1551e&width=768&dpr=3&quality=100&sign=7166be3d6a0182e04b488429ac419240&sv=3)

Fill out the details required and click `**Create Workspace**` Button.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252FVr4nxsJ49fhMjbC4Gp4s%252Fimage.png%3Falt%3Dmedia%26token%3Da3d88765-b55f-4fc5-88a9-72355e5c7c92&width=768&dpr=3&quality=100&sign=406264339d8b3769fe759f170b310d49&sv=3)

Go to a browser window (preferable Chromium based), and open the below URL:

[https://api.postman.com/collections/33708049-43be070a-8630-44bf-8762-17e9551a3250?access\_key=PMAT-01K1WGWPRBYWSB89Q6TWCWJW21](https://api.postman.com/collections/33708049-43be070a-8630-44bf-8762-17e9551a3250?access_key=PMAT-01K1WGWPRBYWSB89Q6TWCWJW21)

The webpage will show raw JSON content of the postman collection exposed via the above URL.

Follow the below steps to save this content to a JSON file:

1.  Select all the content on the webpage.
    
2.  Open a Notepad and paste the JSON content.
    
3.  Save As this file and use the extension \[dot\] JSON to save the file as a JSON file type.
    
4.  Choose the file name as per your requirement. e.g. collection
    
5.  In the end, you will have `**collection.json**` file.
    

Goto Postman and click on `**import**` button towards the top left of the screen inside the workspace created above.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252FTDNFZUBOljCMH0FyKMpP%252Fimage.png%3Falt%3Dmedia%26token%3D18a19e70-55e2-424e-9626-a0f5a0f9bcbb&width=768&dpr=3&quality=100&sign=366caf846acc34f8155238751db04a9f&sv=3)

In the box that appears, drag and drop the `**collection.json**` file created above.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252FwSfJL2yzDU9muRCdwSOt%252Fimage.png%3Falt%3Dmedia%26token%3Df65066c1-581a-47e7-9fc8-cb91ae6a638c&width=768&dpr=3&quality=100&sign=da894fa1faf97b4adaf1c3515e450bb8&sv=3)

Once imported, the collection will look something like below:

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252Fm2wc5UK5ev62eZVNik1h%252Fimage.png%3Falt%3Dmedia%26token%3Dce665816-7e34-470d-934c-935a47e5b8fb&width=768&dpr=3&quality=100&sign=059ff6e910e67c3ab768439a62d91ddc&sv=3)

The collection is developed directly by Bhashini team and the same may change as per new changes that will be introduced over time.

Accessing Variables[](https://dibd-bhashini.gitbook.io/bhashini-apis/download-postman-collection#accessing-variables)

----------------------------------------------------------------------------------------------------------------------

The postman collection has automation done for easy understanding of the integrators. For the same, variables are defined on Collection level.

To access these variables, click the `**Collection Name**` and then click on `**Variables**`.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252FMor6mRsgBk9BhDN3XQAR%252Fimage.png%3Falt%3Dmedia%26token%3Dc66958c1-ec0f-45f0-8e92-dcf1af10026e&width=768&dpr=3&quality=100&sign=229734687637c8467a28774393919eff&sv=3)

This will list down all the variables that are used as a part of different API calls. Details of each variables is given below:

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252FJ0o9B9ZKiHcrXLP4dHbE%252Fimage.png%3Falt%3Dmedia%26token%3Db7ae2324-7c8d-4810-b83d-3c510ca03199&width=768&dpr=3&quality=100&sign=65aa894aff9cec0e79beeb7404fa4add&sv=3)

These variables might change as and when new features will be avaiable as a part of different calls. The collection will have to be imported again to receive the updates.

*   `**ulca_url:**` ULCA Endpoint to send the [Pipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
    
*   `**user_id:**` ID to uniquely identify each integrator as defined [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding#obtaining-user-id)
    .
    
*   `**api_key:**` API Key as generated by the integrator for a specific application as described [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding#api-key-creation)
    .
    
*   `**pipeline_id:**` Pipeline ID obtained by the integrator either via discussion with Bhashini team, ULCA Web, or [Pipeline Search Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call)
    
*   `**callback_url:**` URL that is obtained from the response of [Pipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
     as described [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)
    . This parameter is dynamically allocated with the value as discussed later in this page.
    
*   `**callback_url_feedback:**` Feedback URL that is obtained from the response of [Pipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
     as described [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)
    . This parameter is dynamically allocated with the value as discussed later in this page.
    
*   `**compute_call_authorization_key:**` This is a key parameter which is used for authorization of the [Pipeline Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call)
     and is obtained from the response of [Pipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
     as described [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)
    . This parameter is dynamically allocated with the value as discussed later in this page.
    
*   `**compute_call_authorization_value:**` This is the value of the key above used for authorization of the [Pipeline Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call)
     and is obtained from the response of [Pipeline Config Call](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call)
     as described [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload#parameter-pipelineinferenceapiendpoint)
    . This parameter is dynamically allocated with the value as discussed later in this page.
    
*   `**asr_service_id:**` ASR Service ID is the service ID allocated if **ASR** task is requested by the integrator either in individual task or as a combination of tasks and is dynamically allocated either via running `**With Config Request**` or `**Without Config Request**` as described in [Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)
    .
    
*   `**nmt_service_id:**` NMT Service ID is the service ID allocated if **Translation** task is requested by the integrator either in individual task or as a combination of tasks and is dynamically allocated either via running `**With Config Request**` or `**Without Config Request**` as described in [Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)
    .
    
*   `**tts_service_id:**` TTS Service ID is the service ID allocated if TTS task is requested by the integrator either in individual task or as a combination of tasks and is dynamically allocated either via running `**With Config Request**` or `**Without Config Request**` as described in [Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload)
    .
    
*   `**source_language:**` Source Language takes in [ISO 639 Series code](https://dibd-bhashini.gitbook.io/bhashini-apis)
     of the source language. Integrator defines this language so that the automation scripts written in Postman find appropriate Service IDs and allocated the `**asr_service_id**`, `**nmt_service_id**` and `**tts_service_id**`.
    
*   `**target_language:**` Target Language takes in [ISO 639 Series code](https://dibd-bhashini.gitbook.io/bhashini-apis)
     of the target language. Integrator defines this language so that the automation scripts written in Postman find appropriate Service IDs and allocated the `**asr_service_id**`, `**nmt_service_id**` and `**tts_service_id**`.
    
*   `**base64:**` This is an exemplary base64 content which is used for demo purposes. It can be replaced by the integrator as per their requirements.
    
*   `**inference_input_payload:**` This variable will be allocated with a value automatically after execution of the **Postman Tests** associated with and successful execution of `**Compute Request ASR**`. This is the input payload that is sent for making the `**Compute Request ASR**` API call. This variable will be used in `**Feedback Submission**` API Call. This is used for demo of Feedback Submission for **ASR only**. If any other Compute API call is made, developer should use the same input payload used for that particular Compute API which is then to be used for feedback submission.
    
*   `**inference_output_payload:**` This variable will be allocated with a value automatically after execution of the **Postman Tests** associated with and successful execution of `**Compute Request ASR**`. This is the output/response payload that is received after making a successful `**Compute Request ASR**` API call. This variable will be used in `**Feedback Submission**` API Call. This is used for demo of Feedback Submission for **ASR only**. If any other Compute API call is made, developer should use the same output/response payload received for that particular Compute API which is then to be used for feedback submission.
    
*   `**suggested_inference_output_payload:**` This variable will have exact same structure as **inference\_output\_payload** along with the modified values. The concept is that developer is letting the sever know what should have been the response instead of what has currently being received. For ex. Developer send **Compute Request NMT** API call for doing a translation from **English** to **Hindi**. Developer receives a response which contains **Hindi** text somewhere in that response JSON, but the translated text is slightly incorrect. The incorrect part is corrected in the same place in the output response JSON and this new JSON (with edited and corrected **Hindi** text) is sent back to the server as a part of this variable.
    

### Accessing Automation Scripts[](https://dibd-bhashini.gitbook.io/bhashini-apis/download-postman-collection#accessing-automation-scripts)

The Automation Scripts are written for `**With Config Request**` and `**Without Config Request**` API calls so that appropriate collection variables as described above can be allocated.

Once the Integrator clicks either of the API Call mentioned above, Automation Scripts can be accessed in the `**Tests Tab**` of that API Call as shown below:

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252F5NJCMTU9ODDQvbuU1fd6%252Fimage.png%3Falt%3Dmedia%26token%3Da2359dc8-6e21-4711-8895-6fd216668fa6&width=768&dpr=3&quality=100&sign=e1a01aa712161c4b0ad533058b8e973c&sv=3)

Automation Script for **Without Config Request** API Cal

### Accessing Individual Calls and Combination Calls[](https://dibd-bhashini.gitbook.io/bhashini-apis/download-postman-collection#accessing-individual-calls-and-combination-calls)

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F709902406-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FSuLLfCr6CWwqT0SsqOL1%252Fuploads%252FH5L8TPt6CGsJtucdlvpx%252Fimage.png%3Falt%3Dmedia%26token%3Dd6448b44-db8a-4dd2-a138-359177189832&width=768&dpr=3&quality=100&sign=afc7a5c3bc087adb749def5b12992668&sv=3)

Each individual as well as combination of tasks can be accessed easily.

[PreviousPossible Errors](https://dibd-bhashini.gitbook.io/bhashini-apis/possible-errors)
[NextWebSocket ASR API](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api)

Last updated 1 year ago

---

# Request Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/request-payload.md)
.

Speaker Diarization

Copy

      {
        "pipelineTasks": [\
            {\
                "taskType": "speaker-diarization",\
                "config": {\
                    "serviceId": "{{speaker-diarization_service_id}}"\
                }\
            }\
        ],
        "inputData": {
            "audio": [\
                {\
                    "audioUri": "INSERT_AUDIO_URL_HERE"\
                  // "audioContent": "INSERT_BASE64_AUDIO_HERE"    \
                }\
            ]
        }
    }

This request contains 2 major parameters listed below and detailed further down the section:

1.  pipelineTasks
    
2.  inputData
    

**Parameter:** `**pipelineTasks**`

**Type:** Array

This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes only one dictionary (line 2-9) because integrator wants to do only Audio language detection. `**taskType**` parameter takes `String` that takes the value **speaker-diarization.**

`**config**` is a single key parameter which maps to another object called **serviceId**

The `**serviceId**` parameter is essential for invoking the backend model endpoint for the specified **taskType** with its authentication key. For supported `**serviceId**` and **languages** of the Speaker Diarization service, please visit this link.

[![Logo](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Ficon%252FOSXEcqOtGoQyx1kDbtIW%252Fbhashini.png%3Falt%3Dmedia%26token%3D69f7d83c-b9e6-4bbb-b22b-ccbac2174302&width=48&height=48&sign=262e3d58e5ac67301bee9b9dc8d9d62f&sv=3)Available Models for usage | Bhashini APIsdibd-bhashini.gitbook.io](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage)

**Explore Available serviceIds and supported languages**

`**preProcessors**` is an optional parameter which helps in reducing the background noise and to improve the clarity of the speech signal. These preprocessing steps help in improving the overall performance of speaker diarization API by providing cleaner and more structured input for the core diarization model.

### Parameter: `inputData`[](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/request-payload#parameter-inputdata)

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. in this case, the input is taken via audioUri or audioContent (base64 format).

either user can pass **audioUri** as input or **audioContent** as input.

[PreviousSpeaker Diarization Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call)
[NextResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/response-payload)

Last updated 1 year ago

---

# WebSocket ASR API | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api.md)
.

### Overview[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#overview)

The `ULCASocketClient` is a WebSocket client that enables real-time **Speech-to-Text (ASR)** processing using **BHASHINI's WebSocket API**. This allows audio captured from a microphone to be streamed to Bhashini’s ASR service and receive transcription results **asynchronously**.

* * *

### Prerequisites[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#prerequisites)

Before you begin, ensure you have:

*   Access to a microphone
    
*   Bhashini **API Key** and **Service ID**
    
*   Internet connectivity
    
*   Java Development Kit (JDK) 8 or higher
    
*   Maven project setup
    
*   Java libraries:
    
    *   `socket.io-client` for WebSocket connection
        
    *   `org.json` for JSON processing
        
    

* * *

### Required Dependencies (Maven)[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#required-dependencies-maven)

Copy

    xmlCopyEdit<dependencies>
        <!-- Socket.IO client -->
        <dependency>
            <groupId>io.socket</groupId>
            <artifactId>socket.io-client</artifactId>
            <version>2.1.0</version>
        </dependency>
    
        <!-- JSON library -->
        <dependency>
            <groupId>org.json</groupId>
            <artifactId>json</artifactId>
            <version>20220320</version>
        </dependency>
    </dependencies>

* * *

### Key Components[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#key-components)

1.  **WebSocket Connection**: Connect to Bhashini ASR service.
    
2.  **Audio Capture**: Access microphone and record audio.
    
3.  **Audio Streaming**: Stream audio to the server.
    
4.  **Response Handling**: Receive transcription results from the server.
    

* * *

### Implementation Steps[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#implementation-steps)

#### 1\. Initialize Client[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#id-1.-initialize-client)

Copy

    javaCopyEditULCASocketClient client = new ULCASocketClient("YOUR_WEBSOCKET_SERVER_URL", "YOUR_API_KEY");

#### 2\. Connect to Server[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#id-2.-connect-to-server)

Copy

    javaCopyEditclient.connect();

#### 3\. Configure ASR Task[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#id-3.-configure-asr-task)

Copy

    javaCopyEditJSONObject asrTask = new JSONObject();
    asrTask.put("taskType", "asr");
    
    JSONObject asrConfig = new JSONObject();
    asrConfig.put("serviceId", "YOUR_SERVICE_ID");
    
    JSONObject asrLanguage = new JSONObject();
    asrLanguage.put("sourceLanguage", "en");
    asrConfig.put("language", asrLanguage);
    asrConfig.put("samplingRate", 8000);
    asrConfig.put("audioFormat", "wav");
    asrConfig.put("encoding", JSONObject.NULL);
    
    asrTask.put("config", asrConfig);
    JSONArray taskSequenceArray = new JSONArray().put(asrTask);

#### 4\. Configure Streaming[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#id-4.-configure-streaming)

Copy

    javaCopyEditJSONObject streamingConfig = new JSONObject();
    streamingConfig.put("responseFrequencyInSecs", 2.0);
    streamingConfig.put("responseTaskSequenceDepth", 1);

#### 5\. Start Streaming[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#id-5.-start-streaming)

Copy

    javaCopyEditclient.startStream(taskSequenceArray, streamingConfig);

#### 6\. Start Audio Streaming (VAD-enabled)[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#id-6.-start-audio-streaming-vad-enabled)

The client listens for the `ready` event and then starts audio capture:

Copy

    javaCopyEditclient.startContinuousAudioStreamingWithVAD();

#### 7\. Stop and Disconnect[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#id-7.-stop-and-disconnect)

Copy

    javaCopyEditclient.stop(true);
    client.disconnect();

* * *

### Configuration Parameters[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#configuration-parameters)

#### WebSocket Connection[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#websocket-connection)

Parameter

Description

`serverUrl`

WebSocket server URL (`wss://dhruva-api.bhashini.gov.in`)

`apiKey`

Your Bhashini API key

#### ASR Task Configuration[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#asr-task-configuration)

Parameter

Description

`taskType`

Must be `"asr"`

`serviceId`

Specific ASR service ID

`sourceLanguage`

Language code (e.g., `"en"`)

`samplingRate`

Usually `8000` Hz

`audioFormat`

Format: `"wav"`

`encoding`

Optional, often `null`

#### Streaming Config[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#streaming-config)

Parameter

Description

`responseFrequencyInSecs`

Frequency of intermediate responses

`responseTaskSequenceDepth`

Depth of task-level responses

* * *

### Audio Specifications[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#audio-specifications)

*   **Sampling Rate**: 8000 Hz
    
*   **Bit Depth**: 16-bit
    
*   **Channels**: Mono
    
*   **Encoding**: PCM signed
    

* * *

### Voice Activity Detection (VAD)[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#voice-activity-detection-vad)

VAD ensures only meaningful (spoken) audio is transmitted:

*   Captures audio in real-time
    
*   Identifies speech segments
    
*   Reduces unnecessary data transmission
    

* * *

### API Reference[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#api-reference)

#### Constructor[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#constructor)

Copy

    javaCopyEditULCASocketClient(String serverUrl, String apiKey)

#### Methods[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#methods)

Method

Description

`connect()`

Establish WebSocket connection

`startStream(...)`

Begin audio streaming

`stop(boolean)`

Stop the stream

`disconnect()`

Disconnect from server

`startContinuousAudioStreamingWithVAD()`

Start mic with VAD

`convertByteToInt16(byte[])`

Convert byte array to 16-bit short array

`toUnsignedBytes(short[])`

Convert short array to unsigned bytes

* * *

### WebSocket Events[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#websocket-events)

Event

Trigger

`connect`

Connection successful

`disconnect`

Disconnected

`ready`

Server is ready to receive

`response`

ASR result received

`message`

General server message

`abort`

Server aborted task

`terminate`

Server terminated connection

* * *

### Complete Example[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#complete-example)

Copy

    javaCopyEditpublic static void main(String[] args) {
        try {
            ULCASocketClient client = new ULCASocketClient("YOUR_WS_URL", "YOUR_API_KEY");
            client.connect();
    
            // ASR task config
            JSONObject asrTask = new JSONObject();
            asrTask.put("taskType", "asr");
    
            JSONObject config = new JSONObject();
            config.put("serviceId", "YOUR_SERVICE_ID");
            config.put("language", new JSONObject().put("sourceLanguage", "en"));
            config.put("samplingRate", 8000);
            config.put("audioFormat", "wav");
            config.put("encoding", JSONObject.NULL);
            asrTask.put("config", config);
    
            JSONArray taskSequence = new JSONArray().put(asrTask);
    
            // Streaming config
            JSONObject streamConfig = new JSONObject();
            streamConfig.put("responseFrequencyInSecs", 2.0);
            streamConfig.put("responseTaskSequenceDepth", 1);
    
            client.startStream(taskSequence, streamConfig);
    
            System.out.println("Streaming started. Press Enter to stop...");
            System.in.read();
    
            client.stop(true);
            client.disconnect();
    
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

* * *

### Troubleshooting[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#troubleshooting)

#### Connection Issues[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#connection-issues)

*   Check `serverUrl`
    
*   Validate your API key
    
*   Ensure internet access
    

#### No ASR Output[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#no-asr-output)

*   Confirm `serviceId`
    
*   Check audio format (wav, 8000 Hz)
    
*   Speak clearly/loud enough for VAD
    

#### Debugging Tips[](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api#debugging-tips)

*   Use console logs
    
*   Add `System.out.println` in event handlers
    
*   Watch server `response` events for error codes
    

* * *

[PreviousDownload Postman Collection](https://dibd-bhashini.gitbook.io/bhashini-apis/download-postman-collection)
[NextAppendix](https://dibd-bhashini.gitbook.io/bhashini-apis/appendix)

Last updated 1 year ago

---

# Response Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/response-payload.md)
.

**Complete payload**

Text language Detection response[](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/response-payload#text-language-detection-response)

Copy

    {
        "pipelineResponse": [\
            {\
                "taskType": "txt-lang-detection",\
                "config": null,\
                "output": [\
                    {\
                        "source": "INPUT_TEXT",\
                        "langPrediction": [\
                            {\
                                "langCode": "LANGUAGE_CODE",\
                                "scriptCode": "SCRIPT_CODE",\
                                "langScore": "LANGUAGE_SCORE"\
                            }\
                        ]\
                    }\
                ],\
                "audio": null\
            }\
        ]
    }

The above JSON Response shows the output of the Text language detection task requested by the integrator in that order.

[PreviousRequest payload](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/request-payload)
[NextSpeaker Diarization Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call)

Last updated 1 year ago

---

# Request Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/request-payload.md)
.

Audio language detection

Copy

    { 
      "pipelineTasks": [ \
          { \
            "taskType": "audio-lang-detection",\
            "config": {\
                      "serviceId": "{{ald_service_id}}"\
                      } \
          }\
    ],
    "inputData": {
        "audio": [\
            {\
                "audioContent": "INSERT_BASE64_AUDIO_HERE"\
              //"audioUri": "INSERT_AUDIO_URL_HERE"\
            }\
        ]
    }
    }
    

This request contains 2 major parameters listed below and detailed further down the section:

1.  pipelineTasks
    
2.  inputData
    

### Parameter: `pipelineTasks`[](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/request-payload#parameter-pipelinetasks)

**Type:** Array This parameter takes an array of tasks, in the form of dictionary of `**taskType**` and `**config**`, that are to be done by the integrator. In the above example, `**pipelineTasks**` takes only one dictionary (line 2-9) because integrator wants to do only Audio language detection. `**taskType**` parameter takes `String` that takes the value **audio-lang-detection**

`**config**` is a single key parameter which maps to another object called **serviceId**

serviceId

serviceId parameter identifies the specific service/trained model you want to use.

For serviceId as "**bhashini/iitmandi/audio-lang-detection/gpu**", below are the supported languages-

*   Assamese
    
*   Bengali
    
*   English
    
*   Hindi
    
*   Kannada
    
*   Gujarati
    
*   Malayalam
    
*   Marathi
    
*   Odia
    
*   Punjabi
    
*   Tamil
    
*   Telugu
    

### Parameter: `inputData`[](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/request-payload#parameter-inputdata)

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. in this case, the input is taken via audioUri or audioContent (base64 format).

either user can pass **audioUri** as input or **audioContent** as input.

[PreviousAudio Language Detection Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call)
[NextResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/response-payload)

Last updated 1 year ago

---

# Response Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload.md)
.

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload#complete-payload)

----------------------------------------------------------------------------------------------------------------------------------

Transliteration[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload#transliteration)

Copy

    {
        "pipelineResponse": [\
            {\
                "taskType": "transliteration",\
                "config": null,\
                "output": [\
                    {\
                        "source": "ki",\
                        "target": [\
                            "की",\
                            "कि",\
                            "काई",\
                            "कीई",\
                            "काइ",\
                            "कीइ",\
                            "कै"\
                        ]\
                    }\
                ],\
                "audio": null\
            }\
        ]
    }

The above JSON Response shows the output of the Transliteration task requested by the integrator in that order. Below we will discuss the individual task response as well as combination of tasks in specific sequence.

[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload#undefined)

-----------------------------------------------------------------------------------------------------------

[PreviousRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload)
[NextOptical Character Recognition Call](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call)

Last updated 1 year ago

---

# Audio Language Detection Compute Call | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call.md)
.

**Endpoint:** [**https://dhruva-api.bhashini.gov.in/services/inference/pipeline**](https://dhruva-api.bhashini.gov.in/services/inference/pipeline)

**Additional Headers:**

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.

*   Accept: \*/\*
    
*   Authorization: INSERT\_API\_KEY\_HERE
    
*   Content-Type: application/json
    

Authorization : it is a HTTP header which is used to authenticate the user and permission of the requester to use protected resources. Authorization key value can be obtained from the My Profile section under the App name -> inference API key value after logging in to Bhashini-Udyat.

Accept : it is a HTTP header which is used to specify the types of content they can process. This helps the server understand what kind of response to send back.

Content-Type : it is HTTP header which is used to indicate the media type of the resource being sent. This helps the user understand how to process the content.

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, **Authorization, Accept** and **Content-Type** are the additional parameters sent.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Fuploads%252F6bcKUI8bbbJPXp5GhAjy%252Fimage.png%3Falt%3Dmedia%26token%3Dd3e386b4-7a75-4595-8713-fa5498ee5530&width=768&dpr=3&quality=100&sign=0073a6cfb765ac3b7970416a4ced9fd9&sv=3)

[PreviousResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/response-payload)
[NextRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/request-payload)

Last updated 1 year ago

---

# Speaker Diarization Compute Call | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call.md)
.

**Endpoint:** [**https://dhruva-api.bhashini.gov.in/services/inference/pipeline**](https://dhruva-api.bhashini.gov.in/services/inference/pipeline)

**Additional Headers:**

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.

*   Accept: \*/\*
    
*   Authorization: INSERT\_API\_KEY\_HERE
    
*   Content-Type: application/json
    

Authorization : it is a HTTP header which is used to authenticate the user and permission of the requester to use protected resources. Authorization key value can be obtained from the My Profile section under the App name -> inference API key value after logging in to Bhashini-Udyat.

Accept : it is a HTTP header which is used to specify the types of content they can process. This helps the server understand what kind of response to send back.

Content-Type : it is HTTP header which is used to indicate the media type of the resource being sent. This helps the user understand how to process the content.

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, **Authorization, Accept** and **Content-Type** are the additional parameters sent.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Fuploads%252FKTz7GwBS9bT4VqKvEpab%252Fimage.png%3Falt%3Dmedia%26token%3D76c2b414-5036-4fbb-9a54-badf9d1903a3&width=768&dpr=3&quality=100&sign=8043cc8e361955dccc73fe07f6c91698&sv=3)

[PreviousResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/response-payload)
[NextRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/request-payload)

Last updated 1 year ago

---

# Response Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/response-payload.md)
.

**Complete Payload**

Audio Language Detection response[](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/response-payload#audio-language-detection-response)

Copy

    {
        "pipelineResponse": [\
            {\
                "taskType": "audio-lang-detection",\
                "config": null,\
                "output": [\
                    {\
                        "audio": {\
                            "audioContent": "INPUT_AUDIO_CONTENT",\
                            "audioUri": null\
                        },\
                        "langPrediction": [\
                            {\
                                "langCode": "LANGUAGE_CODE",\
                                "scriptCode": null,\
                                "langScore": null\
                            }\
                        ]\
                    }\
                ],\
                "audio": null\
            }\
        ]
    }

The above JSON Response shows the output of the Audio language detection task requested by the integrator in that order.

[PreviousRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/request-payload)
[NextText Language Detection Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call)

Last updated 1 year ago

---

# Possible Errors | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/possible-errors.md)
.

[PreviousResponse Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/response-payload)
[NextDownload Postman Collection](https://dibd-bhashini.gitbook.io/bhashini-apis/download-postman-collection)

Last updated 2 years ago

---

# Appendix | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/appendix.md)
.

### Full Forms[](https://dibd-bhashini.gitbook.io/bhashini-apis/appendix#full-forms)

ULCA: Universal Language Contribution APIs

ASR: Automatic Speech Recognition

NMT: Neural Machine Translation

TTS: Text to Speech

[PreviousWebSocket ASR API](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api)

Last updated 2 years ago

---

# OCR Modalities Overview | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/ocr-modalities-overview.md)
.

Printed OCR[](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/ocr-modalities-overview#printed-ocr)

This modality is optimized for processing printed documents, typically consisting of structured text in black ink on a white background. These documents are often plain and well-formatted, such as reports, books, or official records. The printed OCR modality is highly efficient at recognizing standard fonts and layouts, making it ideal for digitizing traditional printed materials. Sample image as below.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Fuploads%252F2xOnkDMChSldleAm1W11%252Fimage.png%3Falt%3Dmedia%26token%3Dcfc9e157-e6c3-45e9-8073-6185e3ad5f6c&width=300&dpr=3&quality=100&sign=ac01746332f3846cf216e4a89a928bfe&sv=3)

Scenic OCR[](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/ocr-modalities-overview#scenic-ocr)

Scenic OCR is designed to interpret text present in images that include natural or artificial scenes. These input images often combine visual elements such as landscapes, buildings, or objects with overlaid or embedded text. Scenic OCR is particularly useful for applications such as extracting text from signboards, advertisements, or product packaging, where the background and text are not standardized. Sample image as below.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Fuploads%252FZw6AIRGhRx4MBm6Aj0bM%252Fimage.png%3Falt%3Dmedia%26token%3Df778b023-a259-4ca6-a0ab-3967a67a32b3&width=300&dpr=3&quality=100&sign=ca1f331902a71e417faedb27e3e9eb91&sv=3)

Handwritten OCR[](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/ocr-modalities-overview#handwritten-ocr)

This modality focuses on recognizing text from scanned images of handwritten documents. These inputs typically include variable writing styles, uneven spacing, and inconsistent text alignment. Handwritten OCR is essential for digitizing historical documents, handwritten forms, or personal notes. Advanced techniques in this modality aim to accommodate the diverse characteristics of handwriting to ensure accurate recognition. Sample image as below.

![](https://dibd-bhashini.gitbook.io/bhashini-apis/~gitbook/image?url=https%3A%2F%2F1033188871-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FnW4gyGo8w1tpCSG4RZwV%252Fuploads%252F9IITC7jH6mNWN1kjpyNQ%252Fimage.png%3Falt%3Dmedia%26token%3D2692e620-96cb-4513-a7da-f2b549793e3b&width=300&dpr=3&quality=100&sign=d4f6422fd62823542845123dcb5501bb&sv=3)

Each modality addresses distinct challenges associated with input image types, enabling comprehensive OCR solutions for a wide range of use cases.

[PreviousOptical Character Recognition Call](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call)
[NextRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/request-payload)

Last updated 1 year ago

---

# Response Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/response-payload.md)
.

Optical Character Recognition Response[](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/response-payload#optical-character-recognition-response)

Copy

    {
        "pipelineResponse": [\
            {\
                "taskType": "ocr",\
                "config": null,\
                "output": [\
                    {\
                        "source": "IMAGE_TEXT_CONTENT",\
                        "target": ""\
                    }\
                ],\
                "audio": null\
            }\
        ]
    }

The above JSON Response shows the output of the Optical Character Recognition task requested by the integrator in that order.

#### Parameter: output[](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/response-payload#parameter-pipelinetasks)

**Type:** Array

This parameter takes an array of tasks, in the form of dictionary of `**source and**` `**target**` that are to be done by the integrator. In the above example, `**output**` takes only one dictionary (line 6-11) in which `**output.source**` is a parameter which maps to output text content for the provided input image.

[PreviousRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/request-payload)
[NextAudio Language Detection Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call)

Last updated 1 year ago

---

# Unknown

\# Bhashini APIs

## Bhashini APIs

- \[Overall Understanding of the API Calls\](https://dibd-bhashini.gitbook.io/bhashini-apis/overall-understanding-of-the-api-calls.md): This page will help the integrator understand the number of calls that are to be made to do any specific number of tasks that may or may not include Speech Recognition, Translation and Text to Speech.
- \[Pre-requisites and Onboarding\](https://dibd-bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding.md): This page will help the integrator to get themselves onboarded on Bhashini and get the required API Keys.
- \[Available Models for usage\](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage.md): This page provides the integrator with details about the models available for usage within Bhashini and the Service ID's to be utilized for the languages accordingly.
- \[Pipeline Search Call\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call.md): This page will help the integrator to understand the Pipeline Search API Call. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.
- \[Pipeline Config Call\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call.md): This page will help the integrator to get the details of each pipeline based on Pipeline ID. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.
- \[Request Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload.md): This sub-page helps the integrator to understand two different types of request payload, one without any additional configuration parameters, and one with additional configuration parameters.
- \[Response Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload.md): This sub-page helps the integrator to understand two different types of response payload, based on different request payload.
- \[Pipeline Compute Call\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call.md): This page will help the integrator to get the output of the task sequence requested. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.
- \[Request Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload.md): This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.
- \[Response Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload.md): This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.
- \[Transliteration Config Call\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call.md): This page will help the integrator to get the details of each pipeline based on Pipeline ID. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.
- \[Request Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload.md): This sub-page helps the integrator to understand two different types of request payload, one without any additional configuration parameters, and one with additional configuration parameters.
- \[Response Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload.md)
- \[Transliteration Compute Call\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call.md)
- \[Request Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload.md): This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.
- \[Response Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload.md): This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.
- \[Optical Character Recognition Call\](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call.md): This page will help the integrator to display the texts present in the image. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.
- \[OCR Modalities Overview\](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/ocr-modalities-overview.md): Optical Character Recognition (OCR) technologies are designed to process and interpret text from various input images. Depending on the nature of the input, OCR can be classified into 3 categories.
- \[Request Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/request-payload.md): This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.
- \[Response Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/response-payload.md): This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.
- \[Audio Language Detection Compute Call\](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call.md): This page will help the integrator to identify the language spoken in an audio recording. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.
- \[Request Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/request-payload.md): This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.
- \[Response Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/response-payload.md): This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.
- \[Text Language Detection Compute Call\](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call.md): This page will help the integrator to identify the language in an input texts. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.
- \[Request payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/request-payload.md): This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.
- \[Response Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/response-payload.md): This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.
- \[Speaker Diarization Compute Call\](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call.md): This page will help the integrator to identify the list of speakers spoken in an audio recording. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads
- \[Request Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/request-payload.md): This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.
- \[Response Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/response-payload.md): This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.
- \[Possible Errors\](https://dibd-bhashini.gitbook.io/bhashini-apis/possible-errors.md)
- \[Download Postman Collection\](https://dibd-bhashini.gitbook.io/bhashini-apis/download-postman-collection.md): This page helps the integrator to obtains the JSON of the Postman collection which can be download and imported in Postman.
- \[WebSocket ASR API\](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api.md)
- \[Appendix\](https://dibd-bhashini.gitbook.io/bhashini-apis/appendix.md)

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/overall-understanding-of-the-api-calls.md).

# Overall Understanding of the API Calls

This page will help the integrator understand the number of calls that are to be made to do any specific number of tasks that may or may not include Speech Recognition, Translation and Text to Speech.

> \*\*\*This Bhashini Documentation has been written by Bhashini Team. Please reach out to Bhashini Team on email id (\*\*<mark style="color:orange;">\*\*<digitalindiabhashinidivision@gmail.com>\*\*</mark>\*\*), if you face issues implementing the APIs.\*\*\*

{% hint style="info" %}
Please refer to \[Appendix\](/bhashini-apis/appendix.md) for details on full forms.
{% endhint %}

### What models are available on ULCA? <a href="#what-models-are-available-on-ulca" id="what-models-are-available-on-ulca"></a>

Our Research and Development groups which comprises of different renowned institutes of India like IIT(s), IIIT(s), CDAC etc. have developed models which can do Speech Recognition, Translations, Text to Speech, Optical Character Recognition and many more for Indian languages. Our ULCA Platform exposes these AI/ML models (each identified with an unique Model ID) and a try out page through which integrators can try these models.

{% embed url="<https://bhashini.gov.in/ulca/model/explore-models>" %}
ULCA Repository of Models
{% endembed %}

{% hint style="info" %}
Multiple models could be available that may have similar functionality. For ex. To do Speech Recognition of Hindi language, there may be multiple models available from different institute each uniquely identified by a model ID.
{% endhint %}

## What is a ULCA pipeline?

ULCA Pipeline is a set of tasks that any specific pipeline supports. For example, any specific pipeline (identified by unique pipeline ID) can support the following:

## What is Pipeline ID?

<br>

\* Another pipeline \`P2\`, may support only following Tasks and Task Sequences:\\
  \`\[NMT\]\`\\
  \`\[TTS\]\`\\
  \`\[NMT+TTS\]\`

## When to use which Pipeline ID?

Consider Bhashini provides a few pipelines \`(pipeline ID: P1, P2, etc.)\` that supports some Tasks and Task Sequences.

\*\*Case 1:\*\*\\
If the use case is to do only Translation where an integrator wants to translate a given sentence from one language to another in their app/project. For this use case, a pipeline which supports \`\[NMT\]\` shall be used. Since pipeline \`P1\` and \`P2\` both supports \`\[NMT\]\` task, either \`P1\` or \`P2\` can be used.\\
\\
\*\*Case 2:\*\*\\
Consider another use case, where integrator would also want its users to be able to hear the output along with reading which would require both \`NMT\` and \`TTS\` to be done on the input text, integrator will need a pipeline that supports \`\[NMT+TTS\]\`. Since pipeline \`P1\` and \`P2\` both supports \`\[NMT+TTS\]\`, either \`P1\` or \`P2\` can be used.\\
\\
\*\*Case 3:\*\*\\
Consider yet another use case, where integrator wants to take the input in the form of voice and provide a translated text from one language to another. Integrator will, in this case, needs a pipeline which supports \`\[ASR+NMT\]\`. Since only Pipeline \`P1\` supports \`ASR\` and \`NMT\` together, only \`P1\` can be used.

\*\*Case 4:\*\*\\
Consider yet another use case, where the integrator wants to utilize ASR from Pipeline \`P1\` and \`\[NMT\]\` from Pipeline \`P2\`. The integrator can achieve this as long as both pipelines point to the same API endpoint and are accessible with the same Authorization Keys.\\
\\
Now, from Case 1 and 2, question arises, which one to use, since both are able to do the required task?\\
Integrators will have a detailed description of the capabilities of the pipeline, the models used in those pipelines, domains to which this pipeline may cater well. e.g. Certain pipelines are made for Medical Domain compared to some other pipeline which may cater to Agriculture domain better.\\
Along with description, there is a Search Pipeline API call as well which provides similar information for automation purposes.\\
Based on the understanding obtained from the portal as well as information obtained from the API, the integrator shall be able to determine which pipeline ID to use if multiple pipelines are available which does the same Tasks/Task Sequences.

{% hint style="info" %}
Each of these pipelines are uniquely identified by Pipeline ID.

Each pipeline can support multiple and/or combination of tasks.
{% endhint %}

{% hint style="info" %}
In each of the Task Sequences, order/sequence of tasks is important. e.g. If a pipeline supports \`\[ASR+NMT+TTS\]\`, it will mean that on the input received, first speech recognition will be done, then it will be translated to another language following which Speech in the target language will be generated.
{% endhint %}

## Flow of API calls

Integrator shall do following calls to get the output.

#### \[Pipeline Search API Call \\\[Optional\\\] \](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call)

Pipeline Search API Call helps the integrator to search for pipelines that are available to do specific Tasks or Task Sequences and can be used to filter pipeline search based on different parameters.\\
\\
Integrators will be able to obtain \`Pipeline IDs\` required for their project using this call. &#x20;

#### Pipeline Config Call \\\[Mandatory\]

Once the integrator obtains the Pipeline ID either via Search Call or ULCA web portal, Pipeline Config call shall be sent to Bhashini along with the specific Task/Task Sequence that integrator want to do using this pipeline. Integrator should make sure that the sequence they are sending shall be supported by this pipeline.\\
There are additional configuration parameters which integrators may or may not send to further filter the response of this config call.

#### Pipeline Compute Call \\\[Mandatory\]

Pipeline Compute Call is the final call that will help the integrator to obtain the output of the pipeline task sent.

## Language Codes

Throughout the APIs, Integrators will see that languages are referred by their language codes. For ex. Language Code for Hindi is hi, English is en, and so on.<br>

{% hint style="info" %}
Bhashini follows \[ISO-639 series\](https://www.loc.gov/standards/iso639-2/php/code\_list.php) of language codes.
{% endhint %}

{% hint style="info" %}
Usage of these APIs shall be for the purposes of PoC only. If the Bhashini Sahyogi, Bhashini App Mitra or Bhashini Udyat Mitra wants to use the same on production systems or integrators are charging end-users, please reach out to Bhashini team for the paid version of the APIs and exploring Pricing Plans.
{% endhint %}

---

# Response Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/response-payload.md)
.

**Complete payload**

Speaker Diarization response[](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/response-payload#speaker-diarization-response)

Copy

    {
        "taskType": "speaker-diarization",
        "output": [\
            {\
                "speaker_labels": [\
                    {\
                        "speaker1": [\
                            {\
                                "start_time": 5.44,\
                                "duration": 1.58\
                            }\
                        ]\
                    }\
                ]\
            }\
        ]
    }

The above JSON Response shows the output of the Speaker Diarization task requested by the integrator in that order.

[PreviousRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/request-payload)
[NextPossible Errors](https://dibd-bhashini.gitbook.io/bhashini-apis/possible-errors)

Last updated 1 year ago

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding.md).

# Pre-requisites and Onboarding

This page will help the integrator to get themselves onboarded on Bhashini and get the required API Keys.

## Account Creation

Integrator shall onboard themselves on Bhashini via the link below:\\
\\
Registration: <https://dashboard.bhashini.co.in/user/register>

Once an Integrator reaches the Integrator Registration Page, Integrator has to fill the required details as shown below:

<figure><img src="https://1033188871-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnW4gyGo8w1tpCSG4RZwV%2Fuploads%2FUTt5kbnBCHGu9BG7JPI6%2FScreenshot%202025-02-06%20145922.png?alt=media&amp;token=225c6cd6-60a8-47a8-aeab-40f1c9db9a82" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Please check the spam folder for authentication email too.
{% endhint %}

Users will be able to view their USER ID, API Keys once registered and the registration of the account is approved by DIBD team.

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage.md).

# Available Models for usage

This page provides the integrator with details about the models available for usage within Bhashini and the Service ID's to be utilized for the languages accordingly.

The list below consists of Service ID's to be utilized, each Service ID helps connect with a specific model via the REST APIs of Bhashini. The Service ID's, task type supported by it (such as ASR, Translation, TTS, etc) and the languages supported by it are listed below.

## ASR

<table><thead><tr><th width="99">Sl. No</th><th>Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/iitm/asr-dravidian--gpu--t4</td><td>Telugu, Kannada, Malayalam, Tamil</td><td>IIT Madras</td></tr><tr><td>2</td><td>ai4bharat/conformer-hi-gpu--t4</td><td>Hindi</td><td>AI4Bharat</td></tr><tr><td>3</td><td>ai4bharat/conformer-multilingual-dravidian-gpu--t4</td><td>Kannada, Malayalam, Tamil, Telugu</td><td>AI4Bharat</td></tr><tr><td>4</td><td>ai4bharat/conformer-multilingual-indo\_aryan-gpu--t4</td><td>Hindi, Bengali, Marathi, Urdu, Odia, Punjabi, Gujarati, Sanskrit</td><td>AI4Bharat</td></tr><tr><td>5</td><td>ai4bharat/whisper-medium-en--gpu--t4</td><td>English</td><td>AI4Bharat</td></tr><tr><td>6</td><td>bhashini/ai4bharat/conformer-multilingual-asr</td><td>Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmir, Goan Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu</td><td>AI4Bharat</td></tr><tr><td>7</td><td>bhashini/iitm/asr-indoaryan--gpu--t4</td><td>Gujarati, Odia, Hindi, Marathi, Punjabi, Bengali</td><td>IIT Madras</td></tr><tr><td>8</td><td>bhashini/iitm/asr-misc--gpu--t4</td><td>Bhojpuri, Urdu</td><td>IIT Madras</td></tr><tr><td>9</td><td>bhashini/iisc/asr-mai-t4</td><td>Maithili</td><td>IISC</td></tr><tr><td>10</td><td>bhashini/iisc/asr-bho-t4</td><td>Bhojpuri</td><td>IISC</td></tr><tr><td>11</td><td>bhashini/bodhan/asr-transcribe-flex</td><td>English, Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu, Bhojpuri, Chhattisgarhi, Haryanvi, Bhili</td><td>Bodhan.AI</td></tr><tr><td>12</td><td>bhashini/bodhan/asr-transcribe-core</td><td>English, Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu, Bhojpuri, Bhili</td><td>Bodhan.AI</td></tr></tbody></table>

## Translation

<table><thead><tr><th width="67">Sl. No</th><th width="165">Service ID</th><th width="136">Source Language(s) Supported</th><th width="135">Target Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/iiith/nmt-all</td><td>Hindi, English, Assamese, Awadhi, Bengali, Bhojpuri, Braj, Bodo, Dogri, Konkani, Gondi, Gujarati, Hinglish, Ho, Kannada, Kashmiri, Khasi, Mizo, Maithili, Magahi, Malayalam, Marathi, Manipuri, Nepali, Oriya, Punjabi, Sanskrit, Santali, Sinhala, Sindhi, Tamil, Tulu, Telugu, Urdu, Kangri, Kashmiri</td><td>Hindi, English, Assamese, Awadhi, Bengali, Bhojpuri, Braj, Bodo, Dogri, Konkani, Gondi, Gujarati, Hinglish, Ho, Kannada, Kashmiri, Khasi, Mizo, Maithili, Magahi, Malayalam, Marathi, Manipuri, Nepali, Oriya, Punjabi, Sanskrit, Santali, Sinhala, Sindhi, Tamil, Tulu, Telugu, Urdu, Kangri, Kashmiri</td><td>IIIT Hyderabad</td></tr><tr><td>2</td><td>ai4bharat/indictrans-v2-all-gpu--t4</td><td>English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri,  Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali</td><td>English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali</td><td>AI4Bharat</td></tr><tr><td>3</td><td>Bhashini/IIITH/Trans/V1</td><td>Hindi, English, Telugu, Odia, Gujarati, Urdu,</td><td>Punjabi, Hindi, English, Telugu, Urdu, Gujarati, Odia, Sindhi, Dogri, Kashmiri</td><td>IIIT Hyderabad</td></tr><tr><td>4</td><td>iitb/trilingual-en\_hi\_mr-v1-gpu--t4</td><td>English, Assamese, Marathi, Hindi</td><td>Assamese, Hindi, Bodo, Nepali, English, Marathi, Maithili, Goan Konkani</td><td>IIT Bombay</td></tr><tr><td>5</td><td>bhashini/aukbc/disco-nmt</td><td>Malayalam, Hindi, Tamil</td><td>Malayalam, Hindi, Tamil</td><td>AUKBC</td></tr><tr><td>6</td><td>bhashini/cdac-noida/nmt</td><td>English, Hindi, Tamil, Odia , Bengali</td><td>English, Hindi, Tamil, Odia , Bengali</td><td>CDAC-Noida</td></tr><tr><td>7</td><td>bhashini/cdac-pune/nmt</td><td>English, Kannada, Gujarati,Malayalam</td><td>English, Kannada, Gujarati, Malayalam</td><td>CDAC-Pune</td></tr><tr><td>8</td><td>bhashini/iitkhg/nmt</td><td>Hindi</td><td>Sanskrit</td><td>IIT Kharagpur</td></tr><tr><td>9</td><td>bhashini/bodhan/Indic-trans-v4</td><td>English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri,  Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali</td><td>English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri,  Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali</td><td>Bodhan.AI</td></tr><tr><td>10</td><td>bhashini/iiith/santham/nmt</td><td>Sanskrit</td><td>Tamil</td><td>IIITH</td></tr></tbody></table>

## Transliteration

<table><thead><tr><th width="90">Sl. No</th><th>Service ID</th><th>Source Language(s) Supported</th><th>Target Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>ai4bharat/indicxlit--cpu-fsv2</td><td>English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali, Punjabi, Maithili,  Urdu, Sinhala, Bodo,</td><td>English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri, Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali, Punjabi, Maithili, Urdu, Sinhala,  Bodo</td><td>AI4Bharat</td></tr></tbody></table>

## TTS

<table><thead><tr><th width="86">Sl. No</th><th>Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>Bhashini/IITM/TTS</td><td>Assamese, Bengali, Bodo, Dogri, English, Gujarati, Hindi, Kannada, Goan Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Rajasthani, Sanskrit, Tamil, Telugu, Urdu, Santali (Devanagari Script), Sindhi(Devanagari Script), Kashmiri(Devanagari Script)</td><td>IIT Madras</td></tr><tr><td>2</td><td>ai4bharat/indic-tts-coqui-dravidian-gpu--t4</td><td>Malayalam, Kannada, Tamil, Telugu</td><td>AI4Bharat</td></tr><tr><td>3</td><td>ai4bharat/indic-tts-coqui-indo\_aryan-gpu--t4</td><td>Hindi, Marathi, Assamese, Bengali, Gujarat, Odia, Rajasthani, Punjabi</td><td>AI4Bharat</td></tr><tr><td>4</td><td>ai4bharat/indic-tts-coqui-misc-gpu--t4</td><td>English, Manipuri, Bodo</td><td>AI4Bharat</td></tr><tr><td>5</td><td>Bhashini/IISC/TTS</td><td>Kannada, Telugu, English, Hindi, Marathi, Bengali, Gujarati, Maithili, Bhojpuri, Chhattisgarhi, Magahi</td><td>IISC (SYSPIN)</td></tr><tr><td>6</td><td>bhashini/iisc/sourashtra/tts</td><td>Sourashtra, Tamil</td><td>IISC</td></tr><tr><td>7</td><td>bhashini/bodhan/indic-tts</td><td>English, Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri,  Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali</td><td>Bodhan.AI</td></tr></tbody></table>

## Audio Language Detection

<table><thead><tr><th width="95">Sl. No</th><th>Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/iitmandi/audio-lang-detection/gpu</td><td>Assamese, Bengali, English, Hindi, Kannada, Gujarati, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu</td><td>IIT Mandi</td></tr><tr><td>2</td><td>bhashini/ald</td><td>Goan Konkani, Gujarati, Sanskrit, Telugu, Marathi, Hindi, Odia, Manipuri,  Malayalam, Assamese, Dogri, Santali, Tamil, Sindhi, Bengali, Kashmiri, Kannada, Nepali</td><td>-</td></tr></tbody></table>

## Text Language Detection

<table><thead><tr><th width="93">Sl. No</th><th>Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/indic-lang-detection-all</td><td>Assamese, Bengali, Bodo, Dogri, English, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Oriya, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu</td><td>AI4Bharat</td></tr><tr><td>2</td><td>bhashini/iiiith/indic-lang-detection-all</td><td>Assamese, Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Manipuri, Marathi, Oriya, Punjabi, Tamil, Telugu, Urdu</td><td>IIIT Hyderabad</td></tr><tr><td>3</td><td>bhashini/indic/tld</td><td>Assamese(bng script), Bodo, Bangla, Dogri, English, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu</td><td>-</td></tr></tbody></table>

## Named Entity Recognition

<table><thead><tr><th width="94">Sl. No</th><th>Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/iiith/ner</td><td>Hindi, Urdu, Odia, Telugu</td><td>IIIT Hyderabad</td></tr><tr><td>2</td><td>bhashini/ai4bharat/indic-ner</td><td>Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Telugu, Marathi, Oriya, Punjabi, Tamil</td><td>AI4Bharat</td></tr><tr><td>3</td><td>bhashini/aukbc/ner</td><td>Hindi, Bengali, Marathi, Punjabi, Kannada, Malayalam, Tamil, English</td><td>AUKBC</td></tr></tbody></table>

## OCR

<table><thead><tr><th width="90">Sl. No</th><th>Service ID</th><th>Language(s) Supported</th><th>Modality</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/iiith-ocr-sceneText-all</td><td>Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Manipuri, Marathi, Oriya, Punjabi, Tamil, Telugu, Urdu</td><td>Scene Text</td><td>IIIT Hyderabad</td></tr><tr><td>2</td><td>bhashini/iiith/ocr-hw-bhaasha</td><td>Bengali, Hindi, Malayalam, Marathi, Punjabi, Telugu, Kannada, Tamil</td><td>Handwritten</td><td>IIIT Hyderabad</td></tr><tr><td>3</td><td>bhashini/iiith-bhasha-ocr</td><td>Assamese, Bengali, Bodo, Dogri, English, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithali, Nepali, Malayalam, Manipuri, Marathi, Oriya, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu</td><td>Printed Text</td><td>IIIT Hyderabad</td></tr><tr><td>4</td><td>bhashini/bodhan/indic-doc/ocr</td><td>English, Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu.</td><td>Printed Text</td><td>Bodhan.AI</td></tr><tr><td>5</td><td>bhashini/bodhan/indic-doc/ocr</td><td>English, Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Kannada, Malayalam, Odia, Punjabi, Assamese, Urdu.</td><td>Handwritten Text</td><td>Bodhan.AI</td></tr></tbody></table>

## Speaker Enrollment & Verification

<table><thead><tr><th width="86">SI.No</th><th width="205">Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/iitdharwad/speaker-enrollment</td><td> All Languages</td><td>IIT Dharwad </td></tr><tr><td>2</td><td>bhashini/iitdharwad/speaker-verification</td><td>All Languages</td><td>IIT Dharwad</td></tr></tbody></table>

## Speaker Diarization

<table><thead><tr><th width="86">SI.No</th><th width="221">Service ID</th><th width="204">Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/iisc/speaker-diarization</td><td>All Languages</td><td>IISC</td></tr><tr><td>2</td><td>bhashini/speaker-diarization</td><td>All Languages</td><td>Open Source</td></tr></tbody></table>

## Language Diarization

<table><thead><tr><th width="84">S.No</th><th width="221">Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/nitk/language-diarization</td><td>All Languages</td><td>NITK</td></tr></tbody></table>

## Voice Cloning

<table><thead><tr><th width="79">S.No</th><th width="236.6666259765625">Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/ai4b/indicf5-tts</td><td>Assamese, Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu.</td><td>AI4Bharat</td></tr></tbody></table>

## Lip Sync

<table><thead><tr><th width="78.99996948242188">S.No</th><th width="201.33331298828125">Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/iitm/lip-sync</td><td>All Languages</td><td>IIT Madras</td></tr></tbody></table>

## KWS (Key-Word Spotting)

<table><thead><tr><th width="79">S.No</th><th width="194.33331298828125">Service ID</th><th>Language(s) Supported</th><th>Model Provider</th></tr></thead><tbody><tr><td>1</td><td>bhashini/iitg/kws</td><td>Bengali, Manipuri, Mizo</td><td>IIT Guwahati</td></tr></tbody></table>

---

# Response Payload | Bhashini APIs

For the complete documentation index, see [llms.txt](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt)
. This page is also available as [Markdown](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload.md)
.

Request sent without configuration parameter

Request sent with Configuration Parameter

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#complete-payload)

---------------------------------------------------------------------------------------------------------------------------------

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#complete-payload-1)

Copy

    {
      "languages": [\
        {\
          "sourceLanguage": "en",\
          "targetLanguageList": [\
            "as",\
            "bn",\
            "brx",\
            "gom",\
            "gu",\
            "hi",\
            "kn",\
            "ks",\
            "mai",\
            "ml",\
            "mni",\
            "mr",\
            "ne",\
            "or",\
            "pa",\
            "sa",\
            "sd",\
            "si",\
            "ta",\
            "te",\
            "ur"\
          ]\
        },\
        {\
          "sourceLanguage": "as",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "bn",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "brx",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "gom",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "gu",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "hi",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "kn",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ks",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "mai",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ml",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "mni",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "mr",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ne",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "or",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "pa",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "sa",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "sd",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "si",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ta",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "te",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ur",\
          "targetLanguageList": [\
            "en"\
          ]\
        }\
      ],
      "pipelineResponseConfig": [\
        {\
          "taskType": "transliteration",\
          "config": [\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b0426e74a1c96b489b5441",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "as"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c7c97d6da5111fca0f5e4",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "bn"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b0427878d51611abf708c4",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "brx"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b3c64fa65d5a242f462655",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "gom"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c7c7d2abd9b3200b3003b",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "gu"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c73ce41dcd012c08f07e3",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "hi"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c7e662abd9b3200b3003c",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "kn"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b0429574a1c96b489b5442",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ks"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628cafad2abd9b3200b3003f",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "mai"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628ca83c2abd9b3200b3003e",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ml"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b0429f78d51611abf708c5",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "mni"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c811dd6da5111fca0f5e5",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "mr"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b042a878d51611abf708c6",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ne"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b042b878d51611abf708c7",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "or"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628ca0c52abd9b3200b3003d",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "pa"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b042c374a1c96b489b5443",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "sa"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628cab0ed6da5111fca0f5e8",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "sd"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628cad21d6da5111fca0f5e9",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "si"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c741941dcd012c08f07e4",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ta"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628ca307d6da5111fca0f5e6",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "te"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628ca3e8d6da5111fca0f5e7",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ur"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e599dd811234cfe86bb",\
              "language": {\
                "sourceLanguage": "as",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513eae9dd811234cfe86c3",\
              "language": {\
                "sourceLanguage": "bn",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e949dd811234cfe86c1",\
              "language": {\
                "sourceLanguage": "brx",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e3d9dd811234cfe86b8",\
              "language": {\
                "sourceLanguage": "gom",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513eb5610f2c0e43eeb476",\
              "language": {\
                "sourceLanguage": "gu",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513d39610f2c0e43eeb46e",\
              "language": {\
                "sourceLanguage": "hi",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e7d9dd811234cfe86c0",\
              "language": {\
                "sourceLanguage": "kn",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e4e610f2c0e43eeb471",\
              "language": {\
                "sourceLanguage": "ks",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e6c9dd811234cfe86be",\
              "language": {\
                "sourceLanguage": "mai",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e549dd811234cfe86ba",\
              "language": {\
                "sourceLanguage": "ml",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e84610f2c0e43eeb473",\
              "language": {\
                "sourceLanguage": "mni",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e71610f2c0e43eeb472",\
              "language": {\
                "sourceLanguage": "mr",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e5f9dd811234cfe86bc",\
              "language": {\
                "sourceLanguage": "ne",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e779dd811234cfe86bf",\
              "language": {\
                "sourceLanguage": "or",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e659dd811234cfe86bd",\
              "language": {\
                "sourceLanguage": "pa",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e43610f2c0e43eeb470",\
              "language": {\
                "sourceLanguage": "sa",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e489dd811234cfe86b9",\
              "language": {\
                "sourceLanguage": "sd",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e9d9dd811234cfe86c2",\
              "language": {\
                "sourceLanguage": "si",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e36610f2c0e43eeb46f",\
              "language": {\
                "sourceLanguage": "ta",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513ea6610f2c0e43eeb475",\
              "language": {\
                "sourceLanguage": "te",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e8c610f2c0e43eeb474",\
              "language": {\
                "sourceLanguage": "ur",\
                "targetLanguage": "en"\
              }\
            }\
          ]\
        }\
      ],
      "feedbackUrl": "https://dhruva-api.bhashini.gov.in/services/feedback/submit",
      "pipelineInferenceAPIEndPoint": {
        "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
        "inferenceApiKey": {
          "name": "Authorization",
          "value": "gQNj-sTUJjdkac_hsmJLRlj9DeJzO6Q2qzW5SrshxQAwU635MyHXyAajtExDykfZ"
        },
        "isMultilingualEnabled": true,
        "isSyncApi": true
      },
      "pipelineInferenceSocketEndPoint": {
        "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
        "inferenceApiKey": {
          "name": "Authorization",
          "value": "gQNj-sTUJjdkac_hsmJLRlj9DeJzO6Q2qzW5SrshxQAwU635MyHXyAajtExDykfZ"
        },
        "isMultilingualEnabled": true,
        "isSyncApi": true
      }
    }

Complete Payload shows the JSON structure of the content that is received when Integrator makes a ULCA Config Call without any configuration details as detailed in `Tab 1` of [**Request Payload**](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#without-configuration-parameters)
 This response contains 3 major parameters listed below and detailed further down the section:

1.  [languages](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#parameter-languages)
    
2.  [pipelineResponseConfig](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#parameter-pipelineresponseconfig)
    
3.  [pipelineInferenceAPIEndPoint](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#parameter-pipelineinferenceapiendpoint)
    

### Parameter: `languages`[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#parameter-languages)

This parameter helps integrator to know what languages are available that can be used for the requested pipeline tasks in that sequence. For example, consider scenarios where Integrator requests for either:

*   Individual Task i.e., Transliteration [here](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload#integrators-want-to-do-individual-tasks)
    

For Single Tasks, the understanding is straight-forward that the languages appearing in the response corresponds to that task. e.g.

*   If the integrator wants to do `**only Transliteration**`, the languages appearing shows that Server can do `**Transliteration**`in these languages. In this case, parameters `**sourceLanguage**` and `**targetLanguageList**` means that for the languages appearing in `**targetLanguageList**` are the ones in which Server can do translation FROM the language that appear in `**sourceLanguage**`.
    

Usual format of language for such cases is below:

Supported Languages for requested Pipeline.[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#supported-languages-for-requested-pipeline)

Copy

    "languages": [\
        {\
          "sourceLanguage": "en",\
          "targetLanguageList": [\
            "as",\
            "bn",\
            "brx",\
            "gom",\
            "gu",\
            "hi",\
            "kn",\
            "ks",\
            "mai",\
            "ml",\
            "mni",\
            "mr",\
            "ne",\
            "or",\
            "pa",\
            "sa",\
            "sd",\
            "si",\
            "ta",\
            "te",\
            "ur"\
          ]\
        },\
        {\
          "sourceLanguage": "as",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "bn",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "brx",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "gom",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "gu",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "hi",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "kn",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ks",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "mai",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ml",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "mni",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "mr",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ne",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "or",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "pa",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "sa",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "sd",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "si",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ta",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "te",\
          "targetLanguageList": [\
            "en"\
          ]\
        },\
        {\
          "sourceLanguage": "ur",\
          "targetLanguageList": [\
            "en"\
          ]\
        }\
      ]

### Parameter: `pipelineResponseConfig`[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#parameter-pipelineresponseconfig)

This parameter helps the integrator to obtain the `**Service ID**` for a particular task type and language(s) associated with that task.

The task types appearing here will be the same as the ones that the integrator requested while sending the `**pipelineTasks**` parameter in [Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload)
 Say the language pair chosen is `**Bengali**` to `**Assamese**`. Integrator shall now obtain the Service ID correspondingly in the below manner:

1.  Obtain Service ID for doing `**ASR**` in `**Bengali**`. Line 6 from Dictionary of Line 5-14 below.
    
2.  Obtain Service ID for doing `**Translation**` from `**Bengali**` to `**Assamese**`. Line 49 from Dictionary of Line 48-55 below.
    
3.  Obtain Service ID for doing `**TTS**` in `**Assamese**`. Line 89 from Dictionary of Line 88-98 below.
    

These Service IDs will be used in the [Transliteration Compute Call.](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call)

For each `**taskType**` in the response, there may appear additional configuration parameters that are specific to each `**taskType.**`

Configuration Details and Service IDs for requested pipeline tasks.[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#configuration-details-and-service-ids-for-requested-pipeline-tasks)

Copy

    "pipelineResponseConfig": [\
        {\
          "taskType": "transliteration",\
          "config": [\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b0426e74a1c96b489b5441",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "as"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c7c97d6da5111fca0f5e4",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "bn"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b0427878d51611abf708c4",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "brx"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b3c64fa65d5a242f462655",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "gom"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c7c7d2abd9b3200b3003b",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "gu"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c73ce41dcd012c08f07e3",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "hi"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c7e662abd9b3200b3003c",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "kn"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b0429574a1c96b489b5442",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ks"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628cafad2abd9b3200b3003f",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "mai"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628ca83c2abd9b3200b3003e",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ml"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b0429f78d51611abf708c5",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "mni"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c811dd6da5111fca0f5e5",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "mr"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b042a878d51611abf708c6",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ne"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b042b878d51611abf708c7",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "or"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628ca0c52abd9b3200b3003d",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "pa"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "62b042c374a1c96b489b5443",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "sa"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628cab0ed6da5111fca0f5e8",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "sd"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628cad21d6da5111fca0f5e9",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "si"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628c741941dcd012c08f07e4",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ta"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628ca307d6da5111fca0f5e6",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "te"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "628ca3e8d6da5111fca0f5e7",\
              "language": {\
                "sourceLanguage": "en",\
                "targetLanguage": "ur"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e599dd811234cfe86bb",\
              "language": {\
                "sourceLanguage": "as",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513eae9dd811234cfe86c3",\
              "language": {\
                "sourceLanguage": "bn",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e949dd811234cfe86c1",\
              "language": {\
                "sourceLanguage": "brx",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e3d9dd811234cfe86b8",\
              "language": {\
                "sourceLanguage": "gom",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513eb5610f2c0e43eeb476",\
              "language": {\
                "sourceLanguage": "gu",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513d39610f2c0e43eeb46e",\
              "language": {\
                "sourceLanguage": "hi",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e7d9dd811234cfe86c0",\
              "language": {\
                "sourceLanguage": "kn",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e4e610f2c0e43eeb471",\
              "language": {\
                "sourceLanguage": "ks",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e6c9dd811234cfe86be",\
              "language": {\
                "sourceLanguage": "mai",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e549dd811234cfe86ba",\
              "language": {\
                "sourceLanguage": "ml",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e84610f2c0e43eeb473",\
              "language": {\
                "sourceLanguage": "mni",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e71610f2c0e43eeb472",\
              "language": {\
                "sourceLanguage": "mr",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e5f9dd811234cfe86bc",\
              "language": {\
                "sourceLanguage": "ne",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e779dd811234cfe86bf",\
              "language": {\
                "sourceLanguage": "or",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e659dd811234cfe86bd",\
              "language": {\
                "sourceLanguage": "pa",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e43610f2c0e43eeb470",\
              "language": {\
                "sourceLanguage": "sa",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e489dd811234cfe86b9",\
              "language": {\
                "sourceLanguage": "sd",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e9d9dd811234cfe86c2",\
              "language": {\
                "sourceLanguage": "si",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e36610f2c0e43eeb46f",\
              "language": {\
                "sourceLanguage": "ta",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513ea6610f2c0e43eeb475",\
              "language": {\
                "sourceLanguage": "te",\
                "targetLanguage": "en"\
              }\
            },\
            {\
              "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
              "modelId": "63513e8c610f2c0e43eeb474",\
              "language": {\
                "sourceLanguage": "ur",\
                "targetLanguage": "en"\
              }\
            }\
          ]\
        }\
      ],

### Parameter: `pipelineInferenceAPIEndPoint`[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#parameter-pipelineinferenceapiendpoint)

This parameter helps the integrator to know the details of the [Transliteration Compute Call.](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call)
 where to send (`**callbackURL**` parameter) and shall be sent along with the `**Authorization Key-Value pair**` received under `**inferenceApiKey**` parameter which will be used for authentication of the same.

Details for Actual Inferencing.[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#details-for-actual-inferencing)

Copy

    "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
            "inferenceApiKey": {
                "name": "Authorization",
                "value": "cZVqccgm-LTAzxQVp6jjznmSR5RgKM"
            },
            "isMultilingualEnabled": true,
            "isSyncApi": true
        }

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#complete-payload-2)

-----------------------------------------------------------------------------------------------------------------------------------

Complete Payload[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#complete-payload-3)

Copy

    {
        "languages": [\
            {\
                "sourceLanguage": "en",\
                "targetLanguageList": [\
                    "as",\
                    "bn",\
                    "brx",\
                    "gom",\
                    "gu",\
                    "hi",\
                    "kn",\
                    "ks",\
                    "mai",\
                    "ml",\
                    "mni",\
                    "mr",\
                    "ne",\
                    "or",\
                    "pa",\
                    "sa",\
                    "sd",\
                    "si",\
                    "ta",\
                    "te",\
                    "ur"\
                ]\
            }\
        ],
        "pipelineResponseConfig": [\
            {\
                "taskType": "transliteration",\
                "config": [\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "62b0426e74a1c96b489b5441",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "as"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628c7c97d6da5111fca0f5e4",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "bn"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "62b0427878d51611abf708c4",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "brx"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "62b3c64fa65d5a242f462655",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "gom"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628c7c7d2abd9b3200b3003b",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "gu"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628c73ce41dcd012c08f07e3",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "hi"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628c7e662abd9b3200b3003c",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "kn"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "62b0429574a1c96b489b5442",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "ks"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628cafad2abd9b3200b3003f",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "mai"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628ca83c2abd9b3200b3003e",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "ml"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "62b0429f78d51611abf708c5",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "mni"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628c811dd6da5111fca0f5e5",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "mr"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "62b042a878d51611abf708c6",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "ne"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "62b042b878d51611abf708c7",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "or"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628ca0c52abd9b3200b3003d",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "pa"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "62b042c374a1c96b489b5443",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "sa"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628cab0ed6da5111fca0f5e8",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "sd"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628cad21d6da5111fca0f5e9",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "si"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628c741941dcd012c08f07e4",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "ta"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628ca307d6da5111fca0f5e6",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "te"\
                        }\
                    },\
                    {\
                        "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                        "modelId": "628ca3e8d6da5111fca0f5e7",\
                        "language": {\
                            "sourceLanguage": "en",\
                            "targetLanguage": "ur"\
                        }\
                    }\
                ]\
            }\
        ],
        "feedbackUrl": "https://dhruva-api.bhashini.gov.in/services/feedback/submit",
        "pipelineInferenceAPIEndPoint": {
            "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
            "inferenceApiKey": {
                "name": "Authorization",
                "value": "gQNj-sTUJjdkac_hsmJLRlj9DeJzO6Q2qzW5SrshxQAwU635MyHXyAajtExDykfZ"
            },
            "isMultilingualEnabled": true,
            "isSyncApi": true
        },
        "pipelineInferenceSocketEndPoint": {
            "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
            "inferenceApiKey": {
                "name": "Authorization",
                "value": "gQNj-sTUJjdkac_hsmJLRlj9DeJzO6Q2qzW5SrshxQAwU635MyHXyAajtExDykfZ"
            },
            "isMultilingualEnabled": true,
            "isSyncApi": true
        }
    }

Complete Payload shows the JSON structure of the content that is received when Integrator makes a ULCA Config Call with some configuration details as detailed in `Tab 2` of [Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#with-configuration-parameters)
. Here, the integrator has requested to do a tasks Transliteration in that sequence from `**English**`

### Parameter: `languages`[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#parameter-languages-1)

The understanding of the parameters remains same as in previous tab. Since the languages were already known to the integrator before-hand, therefore, the response contains configuration details for those languages only.

There may occur a possibility that Integrator wants to do any individual task or combination of tasks in a sequence for the languages that are `**not**` supported by that `**pipeline ID**` in which case the following response will be obtained: **Response Code: 400 Bad Request Response Body:**

Copy

    {
        "code": "400 BAD_REQUEST",
        "message": "Sequence of languages not supported",
        "timestamp": "2023-04-14T06:32:12.133+00:00"
    }

In such cases, it is recommended to send Pipeline Config Request without Configuration as shown in `Tab 1` under [Request Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload#without-configuration-parameters)
 Using which Integrators will know what all languages are supported by that pipeline ID.

### Parameter: `pipelineResponseConfig`[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#parameter-pipelineresponseconfig-1)

The understanding of the parameters remains same as in previous tab. Since the languages were already known to the integrator before-hand, therefore, the response contains configuration details for those languages only.

### Parameter: `pipelineInferenceAPIEndPoint`[](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload#parameter-pipelineinferenceapiendpoint-1)

The understanding of the parameters remains same as in previous tab.

[PreviousRequest Payload](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload)
[NextTransliteration Compute Call](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call)

Last updated 1 year ago

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-search-call.md).

# Pipeline Search Call

This page will help the integrator to understand the Pipeline Search API Call. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.

Currently, 4 pipeline IDs are available to used directly as follows:

\* IIT Madras Models: 660fa5bec7fb5b0328229016 \\\[ASR and TTS task types are available in config call for now\]
\* IIT Bombay Models: 660f813c0413087224435d2c \\\[Translation task type are available in config call for now\]
\* IIIT Hyderabad Models: 660f866443e53d4133f65317 \\\[Translation task type are available in config call for now\]
\* Initial Pipeline Models: 64392f96daac500b55c543cd \\\[ASR, Translation, Transliteration and TTS task types are available in config call for now\]

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call.md).

# Pipeline Config Call

This page will help the integrator to get the details of each pipeline based on Pipeline ID. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.

\*\*Endpoint:\*\* <https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline>

\*\*Additional Headers:\*\*

\* userID
\* ulcaApiKey

\*\*Payload:\*\*

\* \[Tab 1: JSON payload without any configuration parameters\](/bhashini-apis/pipeline-config-call/request-payload.md)
\* \[Tab 2: JSON payload with some configuration parameters\](/bhashini-apis/pipeline-config-call/request-payload.md#with-configuration-parameters)

## Additional Headers

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.\\
\\
\*\*\`userID:\`\*\* Uniquely identify the Integrator.\\
\*\*\`ulcaApiKey:\`\*\* to Authenticate this particular userID

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, \*\*userID\*\* and \*\*ulcaApiKey\*\* are the additional parameters sent.

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2FOJuSinbl0qQ6CBddwwe8%2Fimage.png?alt=media&#x26;token=c5cbeadb-8cb2-4949-802c-64e3de0bbf8d" alt="Postman screenshot of additional parameters" width="100%">

Both userID and ulcaApiKey can be obtained from the \*\*My Profile\*\* section after logging in.

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call.md).

# Pipeline Compute Call

This page will help the integrator to get the output of the task sequence requested. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.

\*\*Endpoint:\*\* Endpoint is obtained from the \*\*\`callbackURL\`\*\* parameter under \[\*\*\`pipelineInferenceAPIEnfPoint\`\*\*\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineinferenceapiendpoint) parameter from the Response Payload of \[Pipeline Config Call\](/bhashini-apis/pipeline-config-call.md) as shown \[here.\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineinferenceapiendpoint)

\*\*Additional Headers:\*\*\\
auth parameter key\\
auth parameter value

\*\*Payload:\*\*

\* ASR
\* Translation
\* TTS
\* ASR+Translation
\* Translation+TTS
\* ASR+Translation+TTS

## Additional Headers

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Compute API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.\\
\\
\*\*auth parameter key\*\*: This value is obtained from \*\*\`name\`\*\* parameter under \*\*\`inferenceApiKey\`\*\* under \[\*\*\`pipelineInferenceAPIEnfPoint\`\*\*\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineinferenceapiendpoint).&#x20;

\*\*auth parameter value\*\*: This value is obtained from \*\*\`value\`\*\* parameter under \*\*\`inferenceApiKey\`\*\* under \[\*\*\`pipelineInferenceAPIEnfPoint\`\*\*\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineinferenceapiendpoint).&#x20;

<figure><img src="https://1033188871-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnW4gyGo8w1tpCSG4RZwV%2Fuploads%2Fv9Il636tmGhrOQvqNp0C%2Fspaces\_SuLLfCr6CWwqT0SsqOL1\_uploads\_0KKVeasdrDINiAvokkjE\_image.webp?alt=media&amp;token=954aafc0-faf1-4258-8852-4d748e31ee07" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
To know more about Additional Headers, please refer \[here.\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineinferenceapiendpoint)
{% endhint %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/response-payload.md).

# Response Payload

This sub-page helps the integrator to understand two different types of response payload, based on different request payload.

{% tabs %}
{% tab title="Request sent without configuration parameter" %}

## Complete Payload

<details>

<summary>Complete Payload</summary>

{% code lineNumbers="true" %}

\`\`\`json
{
    "languages": \[\
        {\
            "sourceLanguage": "bn",\
            "targetLanguageList": \[\
                "en",\
                "as",\
                "gu",\
                "hi"              \
            \]\
        },\
        {\
            "sourceLanguage": "en",\
            "targetLanguageList": \[               \
                "ml",\
                "mr",\
                "or",\
                "pa",\
                "ta",\
                "te"\
            \]\
        },       \
        {\
            "sourceLanguage": "hi",\
            "targetLanguageList": \[\
                "en",\
                "as",\
                "bn",\
                "gu",\
                "kn"\
            \]\
        }\
    \],
    "pipelineResponseConfig": \[\
        {\
            "taskType": "asr",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/conformer-multilingual-indo\_aryan-gpu--t4",\
                    "modelId": "6411746956e9de23f65b5426",\
                    "language": {\
                        "sourceLanguage": "bn"\
                    },\
                    "domain": \[\
                        "general"\
                    \]\
                },\
                {\
                    "serviceId": "ai4bharat/conformer-en-gpu--t4",\
                    "modelId": "63ee09c3b95268521c70cd7c",\
                    "language": {\
                        "sourceLanguage": "en"\
                    },\
                    "domain": \[\
                        "general"\
                    \]\
                },\
                {\
                    "serviceId": "ai4bharat/conformer-multilingual-indo\_aryan-gpu--t4",\
                    "modelId": "64117455b1463435d2fbaec4",\
                    "language": {\
                        "sourceLanguage": "hi"\
                    },\
                    "domain": \[\
                        "general"\
                    \]\
                }\
            \]\
        },\
        {\
            "taskType": "tts",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/indic-tts-coqui-misc-gpu--t4",\
                    "modelId": "63f7384c2ff3ab138f88c64e",\
                    "language": {\
                        "sourceLanguage": "en"\
                    },\
                    "supportedVoices": \[\
                        "male",\
                        "female"\
                    \]\
                },\
                {\
                    "serviceId": "ai4bharat/indic-tts-coqui-indo\_aryan-gpu--t4",\
                    "modelId": "6348db0bfd966563f61bc2c0",\
                    "language": {\
                        "sourceLanguage": "as"\
                    },\
                    "supportedVoices": \[\
                        "male",\
                        "female"\
                    \]\
                }\
            \]\
        },\
        {\
            "taskType": "translation",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/indictrans-fairseq-i2e-gpu--t4",\
                    "modelId": "6110f7bc014fa35d5e767c3b",\
                    "language": {\
                        "sourceLanguage": "bn",\
                        "targetLanguage": "en"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indictrans-fairseq-i2i-gpu--t4",\
                    "modelId": "6214b148751fc8007d24084c",\
                    "language": {\
                        "sourceLanguage": "bn",\
                        "targetLanguage": "as"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indictrans-fairseq-e2i-gpu--t4",\
                    "modelId": "6110f7ce014fa35d5e767c3c",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "as"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indictrans-fairseq-e2i-gpu--t4",\
                    "modelId": "6110f7da014fa35d5e767c3d",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "bn"\
                    }\
                }\
            \]\
        }\
    \],
    "pipelineInferenceAPIEndPoint": {
        "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
        "inferenceApiKey": {
            "name": "Authorization",
            "value": "cZVqccgm-LTAzxQVp6jjznmSR5RgKM"
        },
        "isMultilingualEnabled": true,
        "isSyncApi": true
    }
}
\`\`\`

{% endcode %}

</details>

Complete Payload shows the JSON structure of the content that is received when Integrator makes a ULCA Config Call without any configuration details as detailed in \`Tab 1\` of \[\*\*Request Payload\*\*\](/bhashini-apis/pipeline-config-call/request-payload.md)

\*\*Note: The above payload is used for reference. Response may differ based on the pipeline used by the integrator.\*\*\\
\\
This response contains 3 major parameters listed below and detailed further down the section:

1. \[languages\](#parameter-languages)
2. \[pipelineResponseConfig\](#parameter-pipelineresponseconfig)
3. \[pipelineInferenceAPIEndPoint\](#parameter-pipelineinferenceapiendpoint)

### Parameter: \`languages\`

This parameter helps integrator to know what languages are available that can be used for the requested pipeline tasks in that sequence.\\
\\
For example, consider scenarios where Integrator requests for either:

\* Individual Task i.e., either ASR or Translation or TTS as shown \[here\](/bhashini-apis/pipeline-config-call/request-payload.md#integrators-want-to-do-individual-tasks)
\* Combination of Tasks in that sequence i.e.,
  \* ASR+Translation or
  \* Translation+TTS or
  \* ASR+Translation+TTS as shown \[here\](/bhashini-apis/pipeline-config-call/request-payload.md#integrators-want-to-do-combination-of-tasks-in-that-order)

For Single Tasks, the understanding is straight-forward that the languages appearing in the response corresponds to that task. e.g.&#x20;

\* If the integrator wants to do \*\*\`only ASR\`\*\*, the languages appearing shows that Server can do ASR in these languages. In this case, parameters \*\*\`sourceLanguage\`\*\* and \*\*\`targetLanguageList\`\*\* will contain the same value since for ASR involves only one language unlike Translation where source and target (two) languages are involved. In this case, \*\*\`targetLanguageList\`\*\* can safely be ignored and only \*\*\`sourceLanguage\`\*\* can be used.&#x20;
\* If the integrator wants to do \*\*\`only TTS\`\*\*, the languages appearing shows that Server can do TTS in these languages. In this case, parameters \*\*\`sourceLanguage\`\*\* and \*\*\`targetLanguageList\`\*\* will contain the same value since for TTS too only one language is involved. In this case too, \*\*\`targetLanguageList\`\*\* can safely be ignored and only \*\*\`sourceLanguage\`\*\* can be used.

Usual format of language for such cases is below:

<details>

<summary>Supported Languages for requested Pipeline.</summary>

{% code lineNumbers="true" %}

\`\`\`json
"languages": \[\
        {\
            "sourceLanguage": "bn",\
            "targetLanguageList": \[\
                "bn"              \
            \]\
        },\
        {\
            "sourceLanguage": "en",\
            "targetLanguageList": \[               \
                "en"\
            \]\
        },       \
        {\
            "sourceLanguage": "hi",\
            "targetLanguageList": \[\
                "hi"\
            \]\
        }\
    \]
\`\`\`

{% endcode %}

</details>

\* If the integrator wants to do \*\*\`only Translation\`\*\*, the languages appearing shows that Server can do Translation in these languages. In this case, parameters \*\*\`sourceLanguage\`\*\* and \*\*\`targetLanguageList\`\*\* means that for the languages appearing in \*\*\`targetLanguageList\`\*\* are the ones in which Server can do translation FROM the language that appear in \*\*\`sourceLanguage\`\*\*.

For Combination of Tasks, the understanding is that the languages appearing in the response are the ones which Server can cater to, for the complete task sequence sent by the integrator. e.g.

\* If the integrator wants to do \*\*\`ASR and Translation\`\*\* together in that sequence, the languages appearing shows that the Server can do this combination in that sequence for these languages. In this case, the Server would be able to do this combination for the languages appearing in \*\*\`targetLanguageList\`\*\*, if the input is given in the language mentioned in \*\*\`sourceLanguage\`\*\* parameter.
\* If the integrator wants to do \*\*\`Translation and TTS\`\*\* together in that sequence, the languages appearing shows that the Server can do this combination in that sequence for these languages. In this case, the Server would be able to do this combination for the languages appearing in \*\*\`targetLanguageList\`\*\*, if the input is given in the language mentioned in \*\*\`sourceLanguage\`\*\* parameter.
\* If the integrator wants to do \*\*\`ASR, then Translation and then TTS\`\*\* together in that sequence, the languages appearing shows that the Server can do this combination in that sequence for these languages. In this case, the Server would be able to do this combination for the languages appearing in \*\*\`targetLanguageList\`\*\*, if the input is given in the language mentioned in \*\*\`sourceLanguage\`\*\* parameter.

Usual format of language for such cases is below:

<details>

<summary>Supported Languages for requested Pipeline.</summary>

{% code lineNumbers="true" %}

\`\`\`json
"languages": \[\
        {\
            "sourceLanguage": "bn",\
            "targetLanguageList": \[\
                "en",\
                "as",\
                "gu",\
                "hi"              \
            \]\
        },\
        {\
            "sourceLanguage": "en",\
            "targetLanguageList": \[               \
                "ml",\
                "mr",\
                "or",\
                "pa",\
                "ta",\
                "te"\
            \]\
        },       \
        {\
            "sourceLanguage": "hi",\
            "targetLanguageList": \[\
                "en",\
                "as",\
                "bn",\
                "gu",\
                "kn"\
            \]\
        }\
    \]
\`\`\`

{% endcode %}

</details>

### Parameter: \`pipelineResponseConfig\`

This parameter helps the integrator to obtain the \*\*\`Service ID\`\*\* for a particular task type and language(s) associated with that task.

The task types appearing here will be the same as the ones that the integrator requested while sending the \*\*\`pipelineTasks\`\*\* parameter in \[Request Payload\](/bhashini-apis/pipeline-config-call/request-payload.md)\\
e.g., Integrator request for configuration of the combination of ASR, Translation and TTS together, the \*\*\`pipelineResponseConfig\`\*\* parameter in the output will contain the JSON data as shown below. It will contain three dictionaries for each task type ASR, Translation and TTS.\\
If Integrator requested for a combination of ASR and Translation, this parameter would contain JSON data for ASR and Translation only.\\
\\
Now consider, Integrator knows the language for which the combination ASR, Translation and TTS is to be performed (language may be determined by asking the end-user etc.). \\
\\
Say the language pair chosen is \*\*\`Bengali\`\*\* to \*\*\`Assamese\`\*\*.\\
\\
Integrator shall now obtain the Service ID correspondingly in the below manner:

1. Obtain Service ID for doing \*\*\`ASR\`\*\* in \*\*\`Bengali\`\*\*. Line 6 from Dictionary of Line 5-14 below.
2. Obtain Service ID for doing \*\*\`Translation\`\*\* from \*\*\`Bengali\`\*\* to \*\*\`Assamese\`\*\*. Line 49 from Dictionary of Line 48-55 below.
3. Obtain Service ID for doing \*\*\`TTS\`\*\* in \*\*\`Assamese\`\*\*. Line 89 from Dictionary of Line 88-98 below.

These Service IDs will be used in the \[Pipeline Compute Call\](/bhashini-apis/pipeline-compute-call.md).

{% hint style="info" %}
For each \*\*\`taskType\`\*\* in the response, there may appear additional configuration parameters that are specific to each \*\*\`taskType\`\*\*. e.g.,&#x20;

\* As seen below, for \*\*\`taskType ASR\`\*\*, \*\*\`domain\`\*\* parameter appears which helps integrator to understand the domain(s) (general, agriculture, medical etc.), this particular Service ID is capable of providing output for.
\* Similarly, for \*\*\`taskType TTS\`\*\*, \*\*\`supportedVoice\`\*\* parameter appears which helps integrator to understand which all voices are available for a particular language that is serviced by that specific Service ID.
  {% endhint %}

<details>

<summary>Configuration Details and Service IDs for requested pipeline tasks.</summary>

{% code lineNumbers="true" %}

\`\`\`json
"pipelineResponseConfig": \[\
        {\
            "taskType": "asr",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/conformer-multilingual-indo\_aryan-gpu--t4",\
                    "modelId": "6411746956e9de23f65b5426",\
                    "language": {\
                        "sourceLanguage": "bn"\
                    },\
                    "domain": \[\
                        "general"\
                    \]\
                },\
                {\
                    "serviceId": "ai4bharat/conformer-en-gpu--t4",\
                    "modelId": "63ee09c3b95268521c70cd7c",\
                    "language": {\
                        "sourceLanguage": "en"\
                    },\
                    "domain": \[\
                        "general"\
                    \]\
                },\
                {\
                    "serviceId": "ai4bharat/conformer-multilingual-indo\_aryan-gpu--t4",\
                    "modelId": "64117455b1463435d2fbaec4",\
                    "language": {\
                        "sourceLanguage": "hi"\
                    },\
                    "domain": \[\
                        "general"\
                    \]\
                }\
            \]\
        },\
        {\
            "taskType": "translation",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/indictrans-fairseq-i2e-gpu--t4",\
                    "modelId": "6110f7bc014fa35d5e767c3b",\
                    "language": {\
                        "sourceLanguage": "bn",\
                        "targetLanguage": "en"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indictrans-fairseq-i2i-gpu--t4",\
                    "modelId": "6214b148751fc8007d24084c",\
                    "language": {\
                        "sourceLanguage": "bn",\
                        "targetLanguage": "as"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indictrans-fairseq-e2i-gpu--t4",\
                    "modelId": "6110f7ce014fa35d5e767c3c",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "as"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indictrans-fairseq-e2i-gpu--t4",\
                    "modelId": "6110f7da014fa35d5e767c3d",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "bn"\
                    }\
                }\
            \]\
        },\
        {\
            "taskType": "tts",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/indic-tts-coqui-misc-gpu--t4",\
                    "modelId": "63f7384c2ff3ab138f88c64e",\
                    "language": {\
                        "sourceLanguage": "en"\
                    },\
                    "supportedVoices": \[\
                        "male",\
                        "female"\
                    \]\
                },\
                {\
                    "serviceId": "ai4bharat/indic-tts-coqui-indo\_aryan-gpu--t4",\
                    "modelId": "6348db0bfd966563f61bc2c0",\
                    "language": {\
                        "sourceLanguage": "as"\
                    },\
                    "supportedVoices": \[\
                        "male",\
                        "female"\
                    \]\
                }\
            \]\
        }\
    \]
\`\`\`

{% endcode %}

</details>

### Parameter: \`pipelineInferenceAPIEndPoint\`

This parameter helps the integrator to know the details of the \[Pipeline Compute Call\](/bhashini-apis/pipeline-compute-call.md) where to send (\*\*\`callbackURL\`\*\* parameter) and shall be sent along with the \*\*\`Authorization Key-Value pair\`\*\* received under \*\*\`inferenceApiKey\`\*\* parameter which will be used for authentication of the same.

\*\*Note: The above sample config call is used for reference. Response may differ based on the pipeline used by the integrator.\*\*

<details>

<summary>Details for Actual Inferencing.</summary>

{% code lineNumbers="true" %}

\`\`\`json
"pipelineInferenceAPIEndPoint": {
        "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
        "inferenceApiKey": {
            "name": "Authorization",
            "value": "cZVqccgm-LTAzxQVp6jjznmSR5RgKM"
        },
        "isMultilingualEnabled": true,
        "isSyncApi": true
    }
\`\`\`

{% endcode %}

</details>
{% endtab %}

{% tab title="Request sent with Configuration Parameter" %}

## Complete Payload

<details>

<summary>Complete Payload</summary>

{% code lineNumbers="true" %}

\`\`\`json
{
    "languages": \[\
        {\
            "sourceLanguage": "gu",\
            "targetLanguageList": \[\
                "bn"\
            \]\
        }\
    \],
    "pipelineResponseConfig": \[\
        {\
            "taskType": "asr",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/conformer-multilingual-indo\_aryan-gpu--t4",\
                    "modelId": "6411746056e9de23f65b5425",\
                    "language": {\
                        "sourceLanguage": "gu"\
                    },\
                    "domain": \[\
                        "general"\
                    \]\
                }\
            \]\
        },\
        {\
            "taskType": "translation",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/indictrans-fairseq-i2i-gpu--t4",\
                    "modelId": "62023eeb3fc51c3fe32b8c5b",\
                    "language": {\
                        "sourceLanguage": "gu",\
                        "targetLanguage": "bn"\
                    }\
                }\
            \]\
        },\
        {\
            "taskType": "tts",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/indic-tts-coqui-indo\_aryan-gpu--t4",\
                    "modelId": "636e60e586369150cb00432a",\
                    "language": {\
                        "sourceLanguage": "bn"\
                    },\
                    "supportedVoices": \[\
                        "male",\
                        "female"\
                    \]\
                }\
            \]\
        }\
    \],
    "pipelineInferenceAPIEndPoint": {
        "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
        "inferenceApiKey": {
            "name": "Authorization",
            "value": "m-LTAzxQVp6jjznmSR5RgKM"
        },
        "isMultilingualEnabled": true,
        "isSyncApi": true
    }
}
\`\`\`

{% endcode %}

</details>

Complete Payload shows the JSON structure of the content that is received when Integrator makes a ULCA Config Call with some configuration details as detailed in \`Tab 2\` of \[Request Payload\](/bhashini-apis/pipeline-config-call/request-payload.md). Here, the integrator has requested to do a combination of tasks ASR, Translation and TTS in that sequence from \*\*\`Gujarati\`\*\* to \*\*\`Bengali\`\*\*

### Parameter: \`languages\`

The understanding of the parameters remains same as in previous tab.\\
Since the languages were already known to the integrator before-hand, therefore, the response contains configuration details for those languages only.

{% hint style="info" %}
There may occur a possibility that Integrator wants to do any individual task or combination of tasks in a sequence for the languages that are \*\*\`not\`\*\* supported by that \*\*\`pipeline ID\`\*\* in which case the following response will be obtained:\\
\\
\*\*Response Code: 400 Bad Request\*\*\\
\*\*Response Body:\*\*

{% code lineNumbers="true" %}

\`\`\`json
{
    "code": "400 BAD\_REQUEST",
    "message": "Sequence of languages not supported",
    "timestamp": "2023-04-14T06:32:12.133+00:00"
}
\`\`\`

{% endcode %}

In such cases, it is recommended to send Pipeline Config Request without Configuration as shown in \`Tab 1\` under \[Request Payload\](/bhashini-apis/pipeline-config-call/request-payload.md)\\
Using which Integrators will know what all languages are supported by that pipeline ID.
{% endhint %}

### Parameter: \`pipelineResponseConfig\`

The understanding of the parameters remains same as in previous tab.\\
Since the languages were already known to the integrator before-hand, therefore, the response contains configuration details for those languages only.

### Parameter: \`pipelineInferenceAPIEndPoint\`

The understanding of the parameters remains same as in previous tab.
{% endtab %}
{% endtabs %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call.md).

# Transliteration Config Call

This page will help the integrator to get the details of each pipeline based on Pipeline ID. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.

\*\*Endpoint:\*\* <https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline>

\*\*Additional Headers:\*\*

\* userID
\* ulcaApiKey

\*\*Payload:\*\*

\* \[Tab 1: JSON payload without any configuration parameters\](/bhashini-apis/pipeline-config-call/request-payload.md)
\* \[Tab 2: JSON payload with some configuration parameters\](/bhashini-apis/pipeline-config-call/request-payload.md#with-configuration-parameters)

## Additional Headers

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.\\
\\
\*\*\`userID:\`\*\* Uniquely identify the Integrator.\\
\*\*\`ulcaApiKey:\`\*\* to Authenticate this particular userID

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, \*\*userID\*\* and \*\*ulcaApiKey\*\* are the additional parameters sent.

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2FOJuSinbl0qQ6CBddwwe8%2Fimage.png?alt=media&#x26;token=c5cbeadb-8cb2-4949-802c-64e3de0bbf8d" alt="Postman screenshot of additional parameters" width="100%">

Both userID and ulcaApiKey can be obtained from the \*\*My Profile\*\* section after logging in.

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call.md).

# Transliteration Compute Call

- \[Request Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload.md): This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.
- \[Response Payload\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload.md): This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-config-call/request-payload.md).

# Request Payload

This sub-page helps the integrator to understand two different types of request payload, one without any additional configuration parameters, and one with additional configuration parameters.

{% tabs %}
{% tab title="Without configuration parameters" %}

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks" : \[\
        {\
            "taskType" : "asr"\
        },\
        {\
            "taskType": "translation"\
        },\
        {  \
            "taskType": "tts"\
        },\
        \
    \],
    "pipelineRequestConfig" : {
        "pipelineId" : "xxxx8d51ae52cxxxxxxxx"
    }
}
\`\`\`

{% endcode %}

### Parameters

We will now understand about each parameter available as a part of this payload.\\
\\
\*\*taskType\*\*

\*\*Type:\*\* String

\* Line 3-5 for ASR
\* Line 6-8 for Translation
\* Line 9-11 for TTS

#### pipelineTasks

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* as defined above, that are to be done by the integrator. The sequence of tasks matter. In the above example, the configuration that will be returned back in the response will be for tasks ASR, Translation and TTS in that order.\\
\\
Each \`pipelineId\` (discussed below), may support few individual or task sequences as explained \[here\](/bhashini-apis/overall-understanding-of-the-api-calls.md) and \[here\](/bhashini-apis/overall-understanding-of-the-api-calls.md) and detailed out below.&#x20;

#### pipelineId

\*\*Type:\*\* String\\
\\
\`pipelineId\` takes a string value of the specific pipeline integrator wants to use. The pipeline ID can be obtained either via Pipeline Search Call or via ULCA Web based on the description which helps the integrator to understand what a pipeline can or cannot do.\\
Each pipeline ID may support multiple task and task sequences.

The same has been explained \[here\](/bhashini-apis/pipeline-search-call.md) and \[here\](/bhashini-apis/overall-understanding-of-the-api-calls.md).

#### pipelineRequestConfig

\*\*Type:\*\* Dictionary\\
\\
This parameter takes in the configuration requested to do the sequence of tasks defined under parameter \[pipelineTasks\](#pipelinetasks).

### Integrators want to do individual tasks

{% tabs %}
{% tab title="Payload for Only ASR" %}
\*\*\`pipelineTasks\`\*\* array takes only one dictionary with \*\*\`taskType\`\*\* as \*\*\`asr\`\*\*&#x20;

{% code lineNumbers="true" %}

\`\`\`json
"pipelineTasks" : \[\
    {\
        "taskType" : "asr"\
    }\
\]
\`\`\`

{% endcode %}
{% endtab %}

{% tab title="Payload for Only Translation" %}
\*\*\`pipelineTasks\`\*\* array takes only one dictionary with \*\*\`taskType\`\*\* as \*\*\`translation\`\*\*&#x20;

{% code lineNumbers="true" %}

\`\`\`json
"pipelineTasks" : \[\
    {\
        "taskType" : "translation"\
    }\
\]
\`\`\`

{% endcode %}
{% endtab %}

{% tab title="Payload for Only TTS" %}
\*\*\`pipelineTasks\`\*\* array takes only one dictionary with \*\*\`taskType\`\*\* as \*\*\`tts\`\*\*&#x20;

{% code lineNumbers="true" %}

\`\`\`json
"pipelineTasks" : \[\
    {\
        "taskType" : "tts"\
    }\
\]
\`\`\`

{% endcode %}
{% endtab %}
{% endtabs %}

### Integrators want to do combination of tasks in that order

{% tabs %}
{% tab title="ASR then Translation" %}
\*\*\`pipelineTasks\`\*\* array takes two dictionaries with \*\*\`taskType\`\*\* as \*\*\`asr\`\*\* and \*\*\`translation\`\*\* in that sequence.

Requesting Server with this in the \*\*\`pipelineTasks\`\*\* parameter would mean that integrator wants to ask the server to give the configuration details where server will be able to perform \*\*\`ASR\`\*\* and \*\*\`Translation\`\*\* together by first doing ASR on the input audio, generating digital text of that audio and then also able to generate translation on the output of that ASR.

{% code lineNumbers="true" %}

\`\`\`json
"pipelineTasks" : \[\
    {\
        "taskType" : "asr"\
    },\
    {\
        "taskType" : "translation"\
    }\
\]
\`\`\`

{% endcode %}
{% endtab %}

{% tab title="Translation then  TTS" %}

\*\*\`pipelineTasks\`\*\* array takes two dictionaries with \*\*\`taskType\`\*\* as \*\*\`translation\`\*\* and \*\*\`tts\`\*\* in that sequence.

Requesting Server with this in the \*\*\`pipelineTasks\`\*\* parameter would mean that integrator wants to ask the server to give the configuration details where server will be able to perform \*\*\`Translation\`\*\* and \*\*\`TTS\`\*\* together by first doing Translation on the input text, generating translated text in another language and then also able to generate Speech on the output of that translation.&#x20;

{% code lineNumbers="true" %}

\`\`\`json
"pipelineTasks" : \[\
    {\
        "taskType" : "translation"\
    },\
    {\
        "taskType" : "tts"\
    }\
\]
\`\`\`

{% endcode %}
{% endtab %}

{% tab title="ASR Then Translation then TTS " %}

\*\*\`pipelineTasks\`\*\* array takes three dictionaries with \*\*\`taskType\`\*\* as \*\*\`asr\`\*\*, \*\*\`translation\`\*\* and \*\*\`tts\`\*\* in that sequence.

Requesting Server with this in the \*\*\`pipelineTasks\`\*\* parameter would mean that integrator wants to ask the server to give the configuration details where server will be able to perform \*\*\`ASR\`\*\*, \*\*\`Translation\`\*\* and \*\*\`TTS\`\*\* together by first performing \*\*\`ASR\`\*\*, thereby generating digital text from the input audio, then doing \*\*\`Translation\`\*\* on the output of previous ASR, thereby generating digital text in another language and finally doing \*\*\`TTS\`\*\* on the output of previous Translation, thereby generating Speech in the required language.&#x20;

{% code lineNumbers="true" %}

\`\`\`json
"pipelineTasks" : \[\
    {\
        "taskType" : "asr"\
    },\
    {\
        "taskType" : "translation"\
    },\
    {\
        "taskType" : "tts"\
    }\
\]
\`\`\`

{% endcode %}
{% endtab %}
{% endtabs %}
{% endtab %}

{% tab title="With Configuration Parameters" %}

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks": \[\
        {\
            "taskType": "asr",\
            "config": {\
                "language": {\
                    "sourceLanguage": "xx"\
                }\
            }\
        },\
        {\
            "taskType": "translation",\
            "config": {\
                "language": {\
                    "sourceLanguage": "xx",\
                    "targetLanguage": "yy"\
                }\
            }\
        },\
        {\
            "taskType": "tts",\
            "config": {\
                "language": {\
                    "sourceLanguage": "yy"\
                }\
            }\
        },\
        \
    \],
    "pipelineRequestConfig": {
        "pipelineId" : "xxxx8d51ae52cxxxxxxxx"
    }
}
\`\`\`

{% endcode %}

### Parameters

Only additional parameter \`config\` is detailed out below. Rest of the parameters' understanding remains the same as \[#without-configuration-parameters\](#without-configuration-parameters "mention").

#### config

\*\*Type:\*\* dictionary\\
\\
\`config\` parameter is used for sending configuration parameters to the server for each \`taskType\`. Each \`taskType\` may have some common parameters such as \`language\` and some parameters which are specific to each \`taskType\`.

{% hint style="info" %}
Currently, there are no additional \`taskType\` specific parameters. Once added, they will be described here.
{% endhint %}

#### config

{% tabs %}
{% tab title="ASR" %}
\*\*Type:\*\* dictionary

contains:\\
\\
\*\*language\*\*\\
\*\*Type:\*\* dictionary\\
\\
contains:\\
\\
\*\*sourceLanguage\*\*\\
\*\*Type:\*\* String\\
\\
Source Language will take the \[ISO-639 code\](https://bhashini.gitbook.io/bhashini-apis/) of the language as the input. This parameter will tell the server that integrator wants to receive the information and details about Speech Recognition in this specific language.
{% endtab %}

{% tab title="Translation" %}

\*\*Type:\*\* dictionary

contains:\\
\\
\*\*language\*\*\\
\*\*Type:\*\* dictionary\\
\\
contains:\\
\\
\*\*sourceLanguage\*\*\\
\*\*Type:\*\* String\\
\\
Source Language will take the \[ISO-639 code\](https://bhashini.gitbook.io/bhashini-apis/) of the language as the input. This parameter will tell the server that integrator wants to receive the \`Translation\` information where the input can be translated \*\*\`FROM\`\*\* this language to another language specified in the \`targetLanguage\` below.\\
\\
and\\
\\
\*\*targetLanguage\*\*\\
\*\*Type:\*\* String\\
\\
Target Language will also take the \[ISO-639 code\](https://bhashini.gitbook.io/bhashini-apis/) of the language as the input. This parameter will tell the server that integrator wants to receive the \`Translation\` information where the input can be translated \*\*\`TO\`\*\* this language from another language specified un the \`sourceLanguage\` above.

{% hint style="info" %}
If Translation comes after ASR, and ASR is done in, say \`Marathi\`, then Source Language of Translation should be \`Marathi\` (ISO Code \`mr\`) because the output of ASR (Digital text in Marathi) will be fed to Translation Model.\\
\\
However, if Translation is the first task or the only task, integrator shall provide appropriate Source Language based on the use case.
{% endhint %}
{% endtab %}

{% tab title="TTS" %}

\*\*Type:\*\* dictionary

contains:\\
\\
\*\*language\*\*\\
\*\*Type:\*\* dictionary\\
\\
contains:\\
\\
\*\*sourceLanguage\*\*\\
\*\*Type:\*\* String\\
\\
Source Language will take the \[ISO-639 code\](https://bhashini.gitbook.io/bhashini-apis/) of the language as the input. This parameter will tell the server that integrator wants to receive the information and details about converting text to speech for this specific language.

{% hint style="info" %}
If TTS comes after Translation, and Translation is done, say from \`Marathi\` to \`Hindi\`, then Source Language of TTS should be \`Hindi\` (ISO Code \`hi\`) because the output of Translation (Translated text in Hindi) will be fed to Translation Model.\\
\\
However, if Translation is the first task or the only task, integrator shall provide appropriate Source Language based on the use case.
{% endhint %}
{% endtab %}
{% endtabs %}
{% endtab %}
{% endtabs %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/request-payload.md).

# Request Payload

This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.

## Request Payload for Individual Task

{% tabs %}
{% tab title="ASR" %}
{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks": \[\
        {\
            "taskType": "asr",\
            "config": {\
                "language": {\
                    "sourceLanguage": "xx"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                "audioFormat": "wav",\
                "samplingRate": 16000,\
                "preProcessors": \[\
                    "vad"\
                \],\
                "postProcessors": \[\
                    "itn"\
                \]\
            }\
        }\
    \],
    "inputData": {
        "input": \[\
            {\
                "source": null\
            }\
        \],
        "audio": \[\
            {\
                "audioContent": "{{generated\_base64\_content}}"\
            }\
        \]
    }
}
\`\`\`

{% endcode %}

This response contains 2 major parameters listed below and detailed further down the section:

1. pipelineTasks
2. inputData

### Parameter: \`pipelineTasks\`

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. \\
In the above example, \*\*\`pipelineTasks\`\*\* takes only one dictionary (line 3-13) because integrator wants to do only ASR.\\
\\
\*\*\`taskType\`\*\* parameter takes \`String\` that takes the value \*\*\`asr\`\*\*

\*\*\`config\`\*\* parameter takes a \*\*\`Dictionary\`\*\* that contains following parameters:

{% tabs %}
{% tab title="Language" %}
For ASR, \*\*\`language\`\*\* parameter only takes \*\*\`sourceLanguage\`\*\* which accepts \[ISO-639 Series Code\](/bhashini-apis/overall-understanding-of-the-api-calls.md) of the language.
{% endtab %}

{% tab title="Service ID" %}
serviceId parameter is obtained from the \[Pipeline Config Call\](/bhashini-apis/pipeline-config-call.md) \[response\](/bhashini-apis/pipeline-config-call/response-payload.md) as described \[here\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineresponseconfig).
{% endtab %}

{% tab title="Audio Format" %}
\*\*\`audioFormat\`\*\* parameter accepts format of the audio which was recorded by the application.

\* For Android, \*\*\`wav\`\*\* is preferred and
\* For iOS, \*\*\`wav\`\*\* or \*\*\`flac\`\*\* is preferred.&#x20;

However, the Server also accepts other well -known formats such as \*\*\`mp3\`\*\*.
{% endtab %}

{% tab title="Sampling Rate" %}
Sampling Rate is determined by the application at which the audio is recorded. The Server accepts a minimum value of \*\*\`8000\`\*\* for \*\*\`samplingRate\`\*\* parameter.
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Parameters other than \*\*\`taskType\`\*\*, \*\*\`serviceId\`\*\* and \*\*\`config\`\*\* are optional.
{% endhint %}

### Parameter: \`inputData\`

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input either via \*\*\`input\`\*\* parameter or \*\*\`audio\`\*\* parameter depending on the task to be done.\\
Since ASR is done on audio input data, for ASR,&#x20;

\* \*\*\`input\`\*\* parameter is optional, of no use for ASR but
\* \*\*\`audio\`\*\* parameter is mandatory.

\*\*audio\*\* parameter takes \*\*\`audioContent\`\*\* parameter which accepts \*\*\`base64 String\`\*\* of the actual audio captured.&#x20;

{% hint style="info" %}
If \*\*\`audioFormat\`\*\* or/and \*\*\`samplingRate\`\*\* parameter is/are sent, integrator should make sure that these values correspond to the actual recorded audio.
{% endhint %}
{% endtab %}

{% tab title="Translation" %}
{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks": \[\
        {\
            "taskType": "translation",\
            "config": {\
                "language": {\
                    "sourceLanguage": "hi",\
                    "targetLanguage": "en"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                "numTranslation": "True"\
            }\
        }\
    \],
    "inputData": {
        "input": \[\
            {\
                "source": "मेरा नाम विहिर है और मैं भाषाावर्ष यूज कर रहा हूँ"\
            }\
        \],
        "audio": \[\
            {\
                "audioContent": null\
            }\
        \]
    }
}
\`\`\`

{% endcode %}

This response contains 2 major parameters listed below and detailed further down the section:

1. pipelineTasks
2. inputData

### Parameter: \`pipelineTasks\`

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. \\
In the above example, \*\*\`pipelineTasks\`\*\* takes only one dictionary (line 3-12) because integrator wants to do only Translation.\\
\\
\*\*\`taskType\`\*\* parameter takes \`String\` that takes the value \*\*\`translation\`\*\*

\*\*\`config\`\*\* parameter takes a \*\*\`Dictionary\`\*\* that contains following parameters:

{% tabs %}
{% tab title="Language" %}
For Translation, \*\*\`language\`\*\* parameter takes both \*\*\`sourceLanguage\`\*\* and \*\*\`targetLanguage\`\*\* which accepts \[ISO-639 Series Code\](https://bhashini.gitbook.io/bhashini-apis/)\[ \](/bhashini-apis/overall-understanding-of-the-api-calls.md)of the language.
{% endtab %}

{% tab title="Service ID" %}
serviceId parameter is obtained from the \[Pipeline Config Call\](/bhashini-apis/pipeline-config-call.md) \[response\](/bhashini-apis/pipeline-config-call/response-payload.md) as described \[here\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineresponseconfig).
{% endtab %}

{% tab title="numTranslation" %}
numTranslation is a optional parameter which enable the API to translate the numerical data/digit into the respective target language.

this feature is currently enabled only in \*\*ai4bharat/indictrans-v2-all-gpu--t4\*\* service Id and for devanagari script supported languages. Default value is False.
{% endtab %}
{% endtabs %}

### Parameter: \`inputData\`

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input either via \*\*\`input\`\*\* parameter or \*\*\`audio\`\*\* parameter depending on the task to be done.\\
Since Transaltion is done on digital text input data, for Translation,&#x20;

\* \*\*\`input\`\*\* parameter is mandatory and
\* \*\*\`audio\`\*\* parameter is optional and of no use for Translation.

\*\*input\*\* parameter takes \*\*\`source\`\*\* parameter which accepts \*\*\`digital text string\`\*\*.&#x20;
{% endtab %}

{% tab title="TTS" %}
{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks": \[       \
        {\
            "taskType": "tts",\
            "config": {\
                "language": {\
                    "sourceLanguage": "gu"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                "gender": "female",\
                "speed": 1.0, // range between 0.1 to 1.99\
                "samplingRate": 48000               \
            }\
        }\
    \],
    "inputData": {
        "input": \[\
            {\
                "source": "મારું નામ વિહીર છે અને હું ભાષાવર્ષનો ઉપયોગ કરી રહ્યો છું"\
            }\
        \],
        "audio": \[\
            {\
                "audioContent": null\
            }\
        \]
    }
}
\`\`\`

{% endcode %}

This response contains 2 major parameters listed below and detailed further down the section:

1. pipelineTasks
2. inputData

### Parameter: \`pipelineTasks\`

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. \\
In the above example, \*\*\`pipelineTasks\`\*\* takes only one dictionary (line 3-12) because integrator wants to do only TTS.\\
\\
\*\*\`taskType\`\*\* parameter takes \`String\` that takes the value \*\*\`tts\`\*\*

\*\*\`config\`\*\* parameter takes a \*\*\`Dictionary\`\*\* that contains following parameters:

{% tabs %}
{% tab title="Language" %}
For TTS, \*\*\`language\`\*\* parameter only takes \*\*\`sourceLanguage\`\*\* which accepts \[ISO-639 Series Code\](/bhashini-apis/overall-understanding-of-the-api-calls.md) of the language.
{% endtab %}

{% tab title="Service ID" %}
serviceId parameter is obtained from the \[Pipeline Config Call\](/bhashini-apis/pipeline-config-call.md) \[response\](/bhashini-apis/pipeline-config-call/response-payload.md) as described \[here\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineresponseconfig).
{% endtab %}

{% tab title="gender" %}
gender parameter takes a string input which can either be:

\* male
\* female

gender parameter tells the server that integrator is requesting the generated speech in either male or female voice.
{% endtab %}

{% tab title="speed" %}
speed parameter takes a integer input which helps in controlling on how fast the synthesized voice speaks. Range between 0.1 to 1.99

\* Increased speed makes the speech sounds quicker, useful for fast-paced content like alerts or summaries.
\* Decreased speed makes the speech is slower and more deliberate, ideal for accessibility or language learning.
  {% endtab %}

{% tab title="samplingRate" %}
samplingRate parameter takes a integer value which helps in determining the number of audio samples per second in the generated speech output, measured in Hertz (Hz). It's a key parameter that affects both audio quality and file size.
{% endtab %}
{% endtabs %}

### Parameter: \`inputData\`

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input either via \*\*\`input\`\*\* parameter or \*\*\`audio\`\*\* parameter depending on the task to be done.\\
Since TTS is done on digital text input data, for TTS,&#x20;

\* \*\*\`input\`\*\* parameter is mandatory and
\* \*\*\`audio\`\*\* parameter is optional and of no use for TTS.

\*\*input\*\* parameter takes \*\*\`source\`\*\* parameter which accepts \*\*\`digital text string\`\*\*.&#x20;
{% endtab %}
{% endtabs %}

## Request Payload for Combination of Tasks in specific sequence

{% tabs %}
{% tab title="ASR+Translation" %}
{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks": \[\
        {\
            "taskType": "asr",\
            "config": {\
                "language": {\
                    "sourceLanguage": "xx"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                "audioFormat": "flac",\
                "samplingRate": 16000\
            }\
        },\
        {\
            "taskType": "translation",\
            "config": {\
                "language": {\
                    "sourceLanguage": "xx",\
                    "targetLanguage": "yy"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--mfkds"\
            }\
        }\
    \],
    "inputData": {
        "input": \[\
            {\
                "source": null\
            }\
        \],
        "audio": \[\
            {\
                "audioContent": "{{generated\_base64\_content}}"\
            }\
        \]
    }
}
\`\`\`

{% endcode %}

### Parameter: \`pipelineTasks\`

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. \\
In the above example, \*\*\`pipelineTasks\`\*\* takes two dictionaries:

\* Line 3 to 13 i.e., \*\*\`ASR Dictionary\`\*\*
\* Line 14 to 23 i.e., \*\*\`Translation Dictionary\`\*\*

because integrator wants to do \*\*\`ASR\`\*\* of the input voice followed by \*\*\`Translation\`\*\* of the digital text.&#x20;

\*\*\`Line Number 7\`\*\* and \*\*\`Line Number 18\`\*\* are connected with below understanding. Consider a use-case described below:

Integrator wants to \*\*speak\*\* in say \*\*\`Hindi\`\*\* language and wants to \*\*see\*\* the \*\*translated output\*\* in \*\*\`Marathi\`\*\*. For this to happen, integrator has to:

\* Convert the Audio integrator has spoken to digital text i.e., ASR of Hindi
\* Translate this digital Hindi text to Marathi digital text i.e., Translation from Hindi to Marathi

{% hint style="info" %}
Therefore, the \*\*language code\*\* for \*\*\`ASR\`\*\* that is to be inserted in \*\*Line 7\*\*, shall be \*\*\`hi\`\*\*, i.e., \[ISO 639 series\](/bhashini-apis/overall-understanding-of-the-api-calls.md) code for Hindi. Once this Hindi digital text is generated, the same shall be translated to Marathi, therefore the \*\*source language code\*\* for \*\*\`Translation\`\*\* that is to be inserted in \*\*Line 18\*\*, shall also be \*\*\`hi\`\*\*, which means that \*\*language code\*\* in \*\*Line 7\*\* and \*\*Line 18\*\* shall be same.&#x20;

For Target Language the code to be inserted in Line 19 shall be \*\*\`mr\`\*\*, i.e., \[ISO 639 series\](/bhashini-apis/overall-understanding-of-the-api-calls.md) code for Marathi. &#x20;
{% endhint %}

{% hint style="info" %}
Understanding of all other parameters remains same as described above in \[\*\*\`Request Payload for Individual Task\`\*\*\](#request-payload-for-individual-task).
{% endhint %}
{% endtab %}

{% tab title="Translation+TTS" %}

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks": \[\
        {\
            "taskType": "translation",\
            "config": {\
                "language": {\
                    "sourceLanguage": "hi",\
                    "targetLanguage": "yy"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--dddd"\
            }\
        },\
        {\
            "taskType": "tts",\
            "config": {\
                "language": {\
                    "sourceLanguage": "yy"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--csdcxsa",\
                "gender": "female"\
            }\
        }\
    \],
    "inputData": {
        "input": \[\
            {\
                "source": "मेरा नाम विहिर है और मैं भाषाावर्ष यूज कर रहा हूँ"\
            }\
        \],
        "audio": \[\
            {\
                "audioContent": null\
            }\
        \]
    }
}
\`\`\`

{% endcode %}

### Parameter: \`pipelineTasks\`

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. \\
In the above example, \*\*\`pipelineTasks\`\*\* takes two dictionaries:

\* Line 3 to 12 i.e., \*\*\`Translation Dictionary\`\*\*
\* Line 13 to 22 i.e., \*\*\`TTS Dictionary\`\*\*

because integrator wants to do \*\*\`Translation\`\*\* of a digital text followed by \*\*\`TTS\`\*\*.

\*\*\`Line Number 8\`\*\* and \*\*\`Line Number 17\`\*\* are connected with below understanding. Consider a use-case described below:

Integrator wants to \*\*translate\*\* say from \*\*\`Hindi\`\*\* to \*\*\`Marathi\`\*\* language and wants to \*\*hear\*\* the \*\*output\*\* in \*\*\`Marathi\`\*\*. For this to happen, integrator has to:

\* Translate this digital Hindi text to Marathi digital text i.e., Translation from Hindi to Marathi
\* Generate this Marathi text speech i.e., TTS of the Marathi digital text.&#x20;

{% hint style="info" %}
Therefore, the \*\*source language code\*\* for \*\*\`Translation\`\*\* that is to be inserted in \*\*Line 7\*\*, shall be \*\*\`hi\`\*\*, i.e., \[ISO 639 series\](/bhashini-apis/overall-understanding-of-the-api-calls.md) code for Hindi. The \*\*target language code\*\* to be inserted in Line 8 shall be \*\*\`mr\`\*\*, i.e., \[ISO 639 series\](/bhashini-apis/overall-understanding-of-the-api-calls.md) code for Marathi.

Speech shall be generated in Marathi which means the language code to be inserted in \*\*Line 17\*\* shall be \*\*\`mr\`\*\*, same as \*\*Line 8.\*\*&#x20;
{% endhint %}

{% hint style="info" %}
Understanding of all other parameters remains same as described above in \[\*\*\`Request Payload for Individual Task\`\*\*\](#request-payload-for-individual-task).
{% endhint %}
{% endtab %}

{% tab title="ASR+Translation+TTS" %}

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks": \[\
        {\
            "taskType": "asr",\
            "config": {\
                "language": {\
                    "sourceLanguage": "xx"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                "audioFormat": "flac",\
                "samplingRate": 16000\
            }\
        },\
        {\
            "taskType": "translation",\
            "config": {\
                "language": {\
                    "sourceLanguage": "xx",\
                    "targetLanguage": "yy"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--fwsd"\
            }\
        },\
        {\
            "taskType": "tts",\
            "config": {\
                "language": {\
                    "sourceLanguage": "yy"\
                },\
                "serviceId": "xxxxx--ssssss-d-ddd--fvdfg",\
                "gender": "female"\
            }\
        }\
    \],
    "inputData": {
        "input": \[\
            {\
                "source": null\
            }\
        \],
        "audio": \[\
            {\
                "audioContent": "{{generated\_base64\_content}}"\
            }\
        \]
    }
}
\`\`\`

{% endcode %}

### Parameter: \`pipelineTasks\`

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator.\\
In the above example, \*\*\`pipelineTasks\`\*\* takes two dictionaries:

\* Line 3 to 13 i.e., \*\*\`ASR Dictionary\`\*\*
\* Line 14 to 23 i.e., \*\*\`Translation Dictionary\`\*\*
\* Line 24 to 33 i.e., \*\*\`TTS Dictionary\`\*\*

because integrator wants to do \*\*\`ASR\`\*\* of the voice input, then \*\*\`Translation\`\*\* of a digital text followed by \*\*\`TTS\`\*\*.

\*\*\`Line Number 7\`\*\* and \*\*\`Line Number 18\`\*\* are connected and \*\*\`Line Number 19\`\*\* and \*\*\`Line Number 28\`\*\* with below understanding. Consider a use-case described below:

Integrator wants to \*\*speak\*\* in say \*\*\`Hindi\`\*\* language and wants to \*\*hear\*\* the \*\*translated output\*\* in \*\*\`Marathi\`\*\*. For this to happen, integrator has to:

\* Convert the Audio integrator has spoken to digital text i.e., ASR of Hindi
\* Translate this digital Hindi text to Marathi digital text i.e., Translation from Hindi to Marathi
\* Generate this Marathi text speech i.e., TTS of the Marathi digital text.

{% hint style="info" %}
Therefore, the \*\*language code\*\* for \*\*\`ASR\`\*\* that is to be inserted in \*\*Line 7\*\*, shall be \*\*\`hi\`\*\*, i.e., \[ISO 639 series\](/bhashini-apis/overall-understanding-of-the-api-calls.md) code for Hindi. Once this Hindi digital text is generated, the same shall be translated to Marathi, therefore the \*\*source language code\*\* for \*\*\`Translation\`\*\* that is to be inserted in \*\*Line 18\*\*, shall also be \*\*\`hi\`\*\*, which means that \*\*language code\*\* in \*\*Line 7\*\* and \*\*Line 18\*\* shall be same.&#x20;

The \*\*target language code\*\* to be inserted in \*\*Line 19\*\* shall be \*\*\`mr\`\*\*, i.e., \[ISO 639 series\](/bhashini-apis/overall-understanding-of-the-api-calls.md) code for Marathi.

Speech shall be generated in Marathi which means the language code to be inserted in \*\*Line 28\*\* shall be \*\*\`mr\`\*\*, same as \*\*Line 19.\*\*&#x20;
{% endhint %}

{% hint style="info" %}
Understanding of all other parameters remains same as described above in \[\*\*\`Request Payload for Individual Task\`\*\*\](https://bhashini.gitbook.io/bhashini-apis/)\[.\](#request-payload-for-individual-task)
{% endhint %}
{% endtab %}
{% endtabs %}

## Pre-Processors and Post-Processors within Compute Request

{% tabs %}
{% tab title="ASR" %}
In Automatic Speech Recognition (ASR) systems, preprocessors and postprocessors play a crucial role in refining the audio input and enhancing the textual output, respectively. Below, we provide details on the available preprocessors and postprocessors, along with an example of how to configure them in your request body.

\*\*Preprocessors\*\*

\*\*Voice Activity Detection (VAD)\*\*

\* \*\*Syntax:\*\* \`"preProcessors": \["vad"\]\`
\* \*\*Function:\*\* VAD allows audio content longer than 30 seconds to be passed and processed. It helps identify voice activity to ensure that only the detected voice activity is processed, reducing the load and improving the efficiency of the ASR system.

\*\*Denoiser\*\*

\* \*\*Syntax:\*\* \`"preProcessors": \["denoiser"\]\`
\* \*\*Function:\*\* Denoiser helps in improving the accuracy of speech recognition by reducing background noise from audio inputs.

\*\*Postprocessors\*\*

\*\*Hotwords\*\*

\* \*\*Syntax:\*\* \`"postProcessors": \[{"hotword\_list":\["\`पत्रिका\`"\]}\]\`
\* \*\*Function:\*\* A hotword is postprocessor allows users to share a list of keyword or phrase in which the system is trained to recognize with higher priority or accuracy. This helps in enhancing the ASR performance. This feature is only applicable for Hindi and for service Id "bhashini/ai4bharat/conformer-multilingual-asr".

&#x20;      \*\*Example:\*\*  a Hindi news broadcast where words like "पत्रिका" (Magazine) are frequently mentioned. Adding these as hotwords ensures they are transcribed correctly rather than being replaced by phonetically similar but incorrect words

&#x20;\*\*Inverse Text Normalization (ITN)\*\*

\* \*\*Syntax:\*\* \`"postProcessors": \["itn"\]\`
\* \*\*Function:\*\* ITN converts spoken numbers and dates into their written forms. For example, the ASR would output "two thousand and twenty three" as "2023".

\*\*Punctuation\*\*

\* \*\*Syntax:\*\* \`"postProcessors": \["punctuation"\]\`
\* \*\*Function:\*\* This postprocessor adds punctuations to the ASR output, making the text more readable and closer to natural written language.

  \*\*Example:\*\*

  \* ASR Output: "hello how are you"
  \* Punctuation Output: "Hello, how are you?"

The configuration of preprocessors and postprocessors can be included within the \`config\` section of the request body as shown below:

{% code lineNumbers="true" %}

\`\`\`json
"config": {
    "language": {
        "sourceLanguage": "xx"
    },
    "serviceId": "xxxxx--ssssss-d-ddd--dddd",
    "audioFormat": "flac",
    "samplingRate": 16000,
    "preProcessors": \["vad"\],
    "postProcessors": \[{\
                    "hotword\_list": \["पत्रिका", "रंगकर्म", "फिक्र"\]\
                }, "itn", "punctuation"\]
}
\`\`\`

{% endcode %}
{% endtab %}

{% tab title="Translation" %}
In translation (NMT) systems, postprocessors play a crucial role in refining the textual output to meet specific needs. Below, we provide details on the postprocessor available for translation, along with an example of how to configure it in your request body.

\*\*Postprocessors\*\*

\*\*Glossary\*\*

\* \*\*Syntax:\*\* \`"postProcessors": \["glossary"\]\`
\* \*\*Function:\*\* The glossary postprocessor allows users to create a list of glossary terms within Bhashini Udyat under the My Profile Section once logged in. Glossary terms created are unique for each Bhashini Inference API Key generated under app names. This postprocessor ensures that specific nouns and noun phrases have their translations overridden as per the user's glossary.

\*\*Example:\*\*

\* Default Translation: "Digital India Bhashini Division" is translated to "डिजिटल इंडिया भैसिनी प्रभाग".
\* With Glossary Term: If the glossary term between English and Hindi is entered as "डिजिटल इंडिया भाषिणी डिवीज़न", this will override the default translation.

\*\*Link to Access My Profile Page and Generate Keys and Glossary:\*\* \[Bhashini Udyat Profile Page\](https://bhashini.gov.in/ulca/profile)

\*\*Glossary Terms Usage:\*\* Glossary terms help provide customized solutions for domain-specific translations, ensuring accuracy and context relevance in the translated output.

\*\*Example of Glossary Usage:\*\*

\* Case sensitivity handling (Ex: Glossary entry - English to  Hindi as IPO -> आईपीओ).&#x20;
\* Glossary entries will work by default for:
  1. Entered noun/noun phrase (e.g., IPO)
  2. Capitalized case (Ipo)
  3. Lower case (ipo)
  4. Upper case ( IPO)
  5. Reverse case (if आईपीओ is the source, the target is IPO when translating from Hindi to English).

#### Configuration Example

The configuration of the glossary postprocessor can be included within the \`config\` section of the request body as shown below:

{% code lineNumbers="true" %}

\`\`\`json
"config": {
    "language": {
        "sourceLanguage": "hi",
        "targetLanguage": "xx"
    },
    "postProcessors": \["glossary"\]
    "serviceId": "xxxxx--ssssss-d-ddd--dddd"
}
\`\`\`

{% endcode %}
{% endtab %}

{% tab title="TTS" %}
In Text to Speech (TTS) systems, preprocessor, postprocessors play a crucial role in refining the audio output and enhancing the audio quality respectively. Below, we have provide details on the available preprocessor, postprocessors, along with an format of how to configure them in your request body.

\*\*Preprocessors\*\*

\*\*Text Normalization (TN)\*\*

\* \*\*Syntax:\*\* \`"preProcessors": \["text-normalization"\]\`
\* \*\*Function:\*\* It converts numbers and dates into their name forms. For example, the TTS would output "2025" as "two thousand twenty five".

\*\*Postprocessors\*\*

\*\*High Compression\*\*

\* \*\*Syntax:\*\* \`"postProcessors": \["high-compression"\]\`
\* \*\*Function:\*\* This helps minimize audio file size during download without compromising quality, making it suitable for low-bandwidth(network) environment and applications where storage is a primary concern It also speeds up transmission and playback by reducing latency. It gives 64kbps audio.

\*\*Low Compression\*\*

\* \*\*Syntax:\*\* \`"postProcessors": \["low-compression"\]\`
\* \*\*Function:\*\* This helps minimize audio file size during download without a significant loss in audio quality, making it suitable for low-bandwidth(network) environments. It also speeds up transmission and playback by reducing latency. It gives 128kbps audio.
  {% endtab %}
  {% endtabs %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/pipeline-compute-call/response-payload.md).

# Response Payload

This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.

## Complete Payload

<details>

<summary>ASR+Translate+TTS</summary>

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineResponse": \[\
        {\
            "taskType": "asr",\
            "config": {\
                "serviceId": "ai4bharat/conformer-hi-gpu--t4",\
                "language": {\
                    "sourceLanguage": "hi",\
                    "sourceScriptCode": ""\
                },\
                "audioFormat": "flac",\
                "encoding": null,\
                "samplingRate": 16000,\
                "postProcessors": null\
            },\
            "output": \[\
                {\
                    "source": "मेरा नाम महीर है और मैं भाषा यूज़ कर रहा हूँ"\
                }\
            \],\
            "audio": null\
        },\
        {\
            "taskType": "translation",\
            "config": null,\
            "output": \[\
                {\
                    "source": "मेरा नाम महीर है और मैं भाषा यूज़ कर रहा हूँ",\
                    "target": "माझे नाव माहिर आहे आणि मी भाषेच वापरत आहे"\
                }\
            \],\
            "audio": null\
        },\
        {\
            "taskType": "tts",\
            "config": {\
                "language": {\
                    "sourceLanguage": "mr",\
                    "sourceScriptCode": ""\
                },\
                "audioFormat": "wav",\
                "encoding": "base64",\
                "samplingRate": 22050,\
                "postProcessors": null\
            },\
            "output": null,\
            "audio": \[\
                {\
                    "audioContent": "{{returned\_base64\_content}}",\
                    "audioUri": null\
                }\
            \]\
        }\
    \]
}
\`\`\`

{% endcode %}

</details>

The above JSON Response shows the output of the combination of ASR, Translation and TTS task requested by the integrator in that order. Below we will discuss the individual task response as well as combination of tasks in specific sequence.

## Response for Payload sent for Individual Task Request

{% tabs %}
{% tab title="ASR" %}
{% code lineNumbers="true" %}

\`\`\`json
{
    "taskType": "asr",
    "config": {
        "serviceId": "xxxxx--ssssss-d-ddd--dddd",
        "language": {
            "sourceLanguage": "hi",
            "sourceScriptCode": ""
        },
        "audioFormat": "flac",
        "encoding": null,
        "samplingRate": 16000,
        "postProcessors": null
    },
    "output": \[\
        {\
            "source": "मेरा नाम महीर है और मैं भाषा यूज़ कर रहा हूँ"\
        }\
    \],
    "audio": null
}
\`\`\`

{% endcode %}

For \*\*\`individual ASR task request\`\*\* sent by the integrator, the response will contain only one dictionary where \*\*\`taskType\`\*\* will be \*\*\`asr\`\*\*.&#x20;

### Parameter: \`config\`

\*\*\`config\`\*\* parameter returns the configuration details of the output generated.

### Parameter: \`output\`

\*\*\`output\`\*\* parameter

contains

\*\*\`source\`\*\* parameter which gives the actual digital text of the audio sent as a part of the request as detailed \[here\](/bhashini-apis/pipeline-compute-call/request-payload.md).
{% endtab %}

{% tab title="Translation" %}

{% code lineNumbers="true" %}

\`\`\`json
{
    "taskType": "translation",
    "config": null,
    "output": \[\
        {\
            "source": "मेरा नाम महीर है और मैं भाषा यूज़ कर रहा हूँ",\
            "target": "My name is Vihar and I am using BhashaVarsh."\
        }\
    \],
    "audio": null
}
\`\`\`

{% endcode %}

For \*\*\`individual Translation task request\`\*\* sent by the integrator, the response will contain only one dictionary where \*\*\`taskType\`\*\* will be \*\*\`translation\`\*\*.&#x20;

### Parameter: \`config\`

\*\*\`config\`\*\* parameter returns the configuration details of the output generated.

### Parameter: \`output\`

\*\*\`output\`\*\* parameter

contains

\*\*\`source\`\*\* parameter which shows the digital text which was sent as an input as a part of the request.

\*\*\`source\`\*\* parameter which gives the actual digital text of the audio sent as a part of the request as detailed \[here\](/bhashini-apis/pipeline-compute-call/request-payload.md#translation)\[.\](/bhashini-apis/pipeline-compute-call/request-payload.md#translation)
{% endtab %}

{% tab title="TTS" %}
{% code lineNumbers="true" %}

\`\`\`json
{
    "taskType": "tts",
    "config": {
        "language": {
            "sourceLanguage": "mr",
            "sourceScriptCode": ""
        },
        "audioFormat": "wav",
        "encoding": "base64",
        "samplingRate": 22050,
        "postProcessors": null
    },
    "output": null,
    "audio": \[\
        {\
            "audioContent": "{{returned\_base64\_content}}",\
            "audioUri": null\
        }\
    \]
}
\`\`\`

{% endcode %}

For \*\*\`individual TTS task request\`\*\* sent by the integrator, the response will contain only one dictionary where \*\*\`taskType\`\*\* will be \*\*\`tts\`\*\*.&#x20;

### Parameter: \`config\`

\*\*\`config\`\*\* parameter returns the configuration details of the output generated.

### Parameter: \`audio\`

\*\*\`audio\`\*\* parameter

contains

\*\*\`audioContent\`\*\* parameter which gives the \*\*\`base64 encoded content\`\*\* of the audio content generated on the server and returned. The same shall be converted for a \*\*\`wav\`\*\* file which can then be heard by the integrator.
{% endtab %}
{% endtabs %}

## Response for Payload sent for Individual Task Request

{% tabs %}
{% tab title="ASR+Translation" %}
Output of \*\*\`ASR+Translation\`\*\* comes in the form of combination of \*\*\`ASR\`\*\* and \*\*\`Translation\`\*\* dictionary as detailed \[above\](#response-for-payload-sent-for-individual-task-request).

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineResponse": \[\
        {\
            "taskType": "asr",\
            "config": {\
                "serviceId": "xxxxx--ssssss-d-ddd--dddd",\
                "language": {\
                    "sourceLanguage": "hi",\
                    "sourceScriptCode": ""\
                },\
                "audioFormat": "flac",\
                "encoding": null,\
                "samplingRate": 16000,\
                "postProcessors": null\
            },\
            "output": \[\
                {\
                    "source": "मेरा नाम महीर है और मैं भाषावर्ष यूज़ कर रहा हूँ"\
                }\
            \],\
            "audio": null\
        },\
        {\
            "taskType": "translation",\
            "config": null,\
            "output": \[\
                {\
                    "source": "मेरा नाम महीर है और मैं भाषावर्ष यूज़ कर रहा हूँ",\
                    "target": "माझे नाव माहिर आहे आणि मी भाषेचे वर्ष वापरत आहे"\
                }\
            \],\
            "audio": null\
        }\
    \]
}
\`\`\`

{% endcode %}
{% endtab %}

{% tab title="Translation+TTS" %}

Output of \*\*\`Translation+TTS\`\*\* comes in the form of combination of \*\*\`Translation\`\*\* and \*\*\`TTS\`\*\* dictionary as detailed \[above\](#response-for-payload-sent-for-individual-task-request).

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineResponse": \[\
        {\
            "taskType": "translation",\
            "config": null,\
            "output": \[\
                {\
                    "source": "मेरा नाम महीर है और मैं भाषावर्ष यूज़ कर रहा हूँ",\
                    "target": "माझं नाव माहिर आहे आणि मी भाषेचे वर्ष वापरत आहे."\
                }\
            \],\
            "audio": null\
        },\
        {\
            "taskType": "tts",\
            "config": {\
                "language": {\
                    "sourceLanguage": "mr",\
                    "sourceScriptCode": ""\
                },\
                "audioFormat": "wav",\
                "encoding": "base64",\
                "samplingRate": 22050,\
                "postProcessors": null\
            },\
            "output": null,\
            "audio": \[\
                {\
                    "audioContent": "{{generated\_base64\_content}}",\
                    "audioUri": null\
                }\
            \]\
        }\
    \]
}
\`\`\`

{% endcode %}
{% endtab %}

{% tab title="ASR+Translation+TTS" %}

Output of ASR+Translation+TTS comes in the form of combination of \*\*\`ASR\`\*\*, \*\*\`Translation\`\*\* and \*\*\`TTS\`\*\* dictionary as detailed \[above\](#response-for-payload-sent-for-individual-task-request).

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineResponse": \[\
        {\
            "taskType": "asr",\
            "config": {\
                "serviceId": "ai4bharat/conformer-hi-gpu--t4",\
                "language": {\
                    "sourceLanguage": "hi",\
                    "sourceScriptCode": ""\
                },\
                "audioFormat": "flac",\
                "encoding": null,\
                "samplingRate": 16000,\
                "postProcessors": null\
            },\
            "output": \[\
                {\
                    "source": "मेरा नाम महीर है और मैं भाषा वर्ष यूज़ कर रहा हूँ"\
                }\
            \],\
            "audio": null\
        },\
        {\
            "taskType": "translation",\
            "config": null,\
            "output": \[\
                {\
                    "source": "मेरा नाम महीर है और मैं भाषा वर्ष यूज़ कर रहा हूँ",\
                    "target": "माझे नाव माहिर आहे आणि मी भाषेचे वर्ष वापरत आहे"\
                }\
            \],\
            "audio": null\
        },\
        {\
            "taskType": "tts",\
            "config": {\
                "language": {\
                    "sourceLanguage": "mr",\
                    "sourceScriptCode": ""\
                },\
                "audioFormat": "wav",\
                "encoding": "base64",\
                "samplingRate": 22050,\
                "postProcessors": null\
            },\
            "output": null,\
            "audio": \[\
                {\
                    "audioContent": "{{generated\_base64\_content}}",\
                    "audioUri": null\
                }\
            \]\
        }\
    \]
}
\`\`\`

{% endcode %}
{% endtab %}
{% endtabs %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/request-payload.md).

# Request Payload

This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.

{% tabs %}
{% tab title="Optical Character Recognition" %}

\`\`\`postman\_json
{
    "pipelineTasks": \[\
        {\
            "taskType": "ocr",\
            "config": {\
                "language": {\
                    "sourceLanguage": "ta"\
                },\
                "serviceId": "{{ocr\_service\_id}}",\
                "textDetection":"False"\
            }\
        }\
    \],
    "inputData": {
        "image": \[\
            {\
            "imageUri": "INSERT\_IMAGE\_URL\_HERE"\
            "imageContent": "INSERT\_BASE64\_IMAGECONTENT\_HERE"\
             \
            }\
        \]
    }
}
\`\`\`

{% endtab %}
{% endtabs %}

This request contains 2 major parameters listed below and detailed further down the section:

1. pipelineTasks
2. inputData

#### Parameter: \`pipelineTasks\` <a href="#parameter-pipelinetasks" id="parameter-pipelinetasks"></a>

\*\*Type:\*\* Array

This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. In the above example, \*\*\`pipelineTasks\`\*\* takes only one dictionary (line 2-9) because integrator wants to do only Audio language detection. \*\*\`taskType\`\*\* parameter takes \`String\` that takes the value \*\*ocr\*\*

\*\*\`config\`\*\* is a single key parameter which maps to another object called \*\*serviceId\*\*

\*\*\`sourceLanguage\`\*\* is a key parameter which defines the output language in which the texts displays

\*\*\`textDetection\`\*\*&#x69;s a key parameter which decides whether to enable or disable the inbuilt preprocessor (word-detector). it is of a Boolean value. this parameter should be sent in request body when the service ID is bhashini/iiith-bhasha-ocr.&#x20;

in other 2 cases, pre processor should be sent as word detector to retrieve a clear output text content.

{% tabs %}
{% tab title="Service Id" %}
serviceId parameter identifies the specific service/trained model you want to use.

The \*\*bhashini/iiith-bhasha-ocr\*\* serviceId is used for printed text images.

For serviceId as "\*\*bhashini/iiith-bhasha-ocr\*\*", below are the supported languages-

• Assamese

• Bengali

• English

• Gujarati

• Hindi

• Kannada

• Malayalam

• Manipuri

• Marathi

• Oriya

• Punjabi

• Tamil

• Telugu

The \*\*bhashini/iiith-ocr-sceneText-all\*\* serviceId is used for scene text images.

For serviceId as "\*\*bhashini/iiith-ocr-sceneText-all\*\*", below are the supported languages-

• Assamese

• Bengali

• Gujarati

• Hindi

• Kannada

• Malayalam

• Manipuri

• Marathi

• Oriya

• Punjabi

• Tamil

• Telugu

• Urdu

The \*\*bhashini/iiith-ocr-hw-all\*\* serviceId is used for hand written images.

For serviceId as "\*\*bhashini/iiith-ocr-hw-all\*\*", below are the supported languages-

• Assamese

• Bengali

• English

• Gujarati

• Hindi

• Kannada

• Malayalam

• Manipuri

• Marathi

• Oriya

• Punjabi

• Tamil

• Telugu

• Urdu
{% endtab %}
{% endtabs %}

#### Parameter: \`inputData\` <a href="#parameter-inputdata" id="parameter-inputdata"></a>

inputData Parameter takes the actual input from the integrator on which the individual task has to be done.  in this case, the input is taken via imageUri or imageContent (base64 format).

{% hint style="info" %}
either user can pass \*\*imageUri\*\* as input or \*\*imageContent\*\* as input.
{% endhint %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call.md).

# Optical Character Recognition Call

This page will help the integrator to display the texts present in the image. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.

\*\*Endpoint:\*\* \[\*\*https://dhruva-api.bhashini.gov.in/services/inference/pipeline\*\*\](https://dhruva-api.bhashini.gov.in/services/inference/pipeline)

\*\*Additional Headers:\*\*

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.

\* Accept: \\\*/\\\*
\* Authorization: INSERT\\\_API\\\_KEY\\\_HERE
\* Content-Type: application/json

Authorization : it is a HTTP header which is used to authenticate the user and permission of the requester to use protected resources. Authorization key value can be obtained from the My Profile section under the App name -> inference API key value after logging in to Bhashini-Udyat.

Accept : it is a HTTP header which is used to specify the types of content they can process. This helps the server understand what kind of response to send back.

Content-Type : it is HTTP header which is used to indicate the media type of the resource being sent. This helps the user understand how to process the content.

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, \*\*Authorization, Accept\*\* and \*\*Content-Type\*\* are the additional parameters sent.

<figure><img src="https://1033188871-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnW4gyGo8w1tpCSG4RZwV%2Fuploads%2F9GuKNajN8uWpPAI9uvEZ%2Fimage.png?alt=media&amp;token=fcdf1bdd-9c0a-489e-b2f4-c764592f6ec6" alt=""><figcaption></figcaption></figure>

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/request-payload.md).

# Request Payload

This sub-page helps the integrator to understand two different types of request payload, one without any additional configuration parameters, and one with additional configuration parameters.

{% tabs %}
{% tab title="Without configuration parameters" %}
{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks" : \[\
        \
        {\
            "taskType": "transliteration"\
        }\
        \
    \],
    "pipelineRequestConfig" : {
        "pipelineId" : "xxxx8d51ae52cxxxxxxxx"
    }
}
\`\`\`

{% endcode %}

### Parameters

We will now understand about each parameter available as a part of this payload.\\
\\
\*\*taskType\*\*

\*\*Type:\*\* String

\* Line 4-6 for Transliteration

#### pipelineTasks

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* as defined above, that are to be done by the integrator. The sequence of tasks matter. In the above example, the configuration that will be returned back in the response will be for tasks ASR, Translation and TTS in that order.\\
\\
Each \`pipelineId\` (discussed below), may support few individual or task sequences as explained \[here\](/bhashini-apis/overall-understanding-of-the-api-calls.md) and \[here\](/bhashini-apis/overall-understanding-of-the-api-calls.md) and detailed out below.&#x20;

#### pipelineId

\*\*Type:\*\* String\\
\\
\`pipelineId\` takes a string value of the specific pipeline integrator wants to use. The pipeline ID can be obtained either via Pipeline Search Call or via ULCA Web based on the description which helps the integrator to understand what a pipeline can or cannot do.\\
Each pipeline ID may support multiple task and task sequences.

The same has been explained \[here\](/bhashini-apis/pipeline-search-call.md) and \[here\](/bhashini-apis/overall-understanding-of-the-api-calls.md).

#### pipelineRequestConfig

\*\*Type:\*\* Dictionary\\
\\
This parameter takes in the configuration requested to do the sequence of tasks defined under parameter \[pipelineTasks\](#pipelinetasks).

###

{% endtab %}

{% tab title="With Configuration Parameters" %}
{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks": \[\
        {\
            "taskType": "transliteration",\
            "config": {\
                "language": {\
                    "sourceLanguage": "en"\
                }\
            }\
        }\
        \
    \],
    "pipelineRequestConfig": {
        "pipelineId" : "xxxx8d51ae52cxxxxxxxx"
    }
}
\`\`\`

{% endcode %}

### Parameters

Only additional parameter \`config\` is detailed out below. Rest of the parameters' understanding remains the same as \[#without-configuration-parameters\](#without-configuration-parameters "mention").

#### config

\*\*Type:\*\* dictionary\\
\\
\`config\` parameter is used for sending configuration parameters to the server for each \`taskType\`. Each \`taskType\` may have some common parameters such as \`language\` and some parameters which are specific to each \`taskType\`.

{% hint style="info" %}
Currently, there are no additional \`taskType\` specific parameters. Once added, they will be described here.
{% endhint %}

#### config

{% tabs %}
{% tab title="Transliteration" %}
\*\*Type:\*\* dictionary

contains:\\
\\
\*\*language\*\*\\
\*\*Type:\*\* dictionary\\
\\
contains:\\
\\
\*\*sourceLanguage\*\*\\
\*\*Type:\*\* String\\
\\
Source Language will take the \[ISO-639 code\](https://bhashini.gitbook.io/bhashini-apis/) of the language as the input. This parameter will tell the server that integrator wants to receive the information and details about Speech Recognition in this specific language.
{% endtab %}
{% endtabs %}
{% endtab %}
{% endtabs %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/request-payload.md).

# Request payload

This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.

{% tabs %}
{% tab title="Text Language Detection payload" %}
{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineTasks": \[\
        {\
            "taskType": "txt-lang-detection",\
            "config": {\
                "serviceId": "{{tld\_service\_id}}"\
            }\
        }\
    \],
    "inputData": {
        "input": \[\
            {\
                "source": "INSERT\_TEXT\_HERE"\
            }\
        \]
    }
}

\`\`\`

{% endcode %}
{% endtab %}
{% endtabs %}

This request contains 2 major parameters listed below and detailed further down the section:

1. pipelineTasks
2. inputData

### Parameter: \`pipelineTasks\`

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. \\
In the above example, \*\*\`pipelineTasks\`\*\* takes only one dictionary (line 2-9) because integrator wants to do only text language detection.\\
\\
\*\*\`taskType\`\*\* parameter takes \`String\` that takes the value \*\*txt-lang-detection\*\*

\*\*\`config\`\*\* is a single key parameter which maps to another object called serviceId.

{% tabs %}
{% tab title="Service ID" %}
serviceId parameter identifies the specific service/trained model you want to use.

For serviceId as "\*\*bhashini/indic-lang-detection-all\*\*", below are the supported languages-

• Assamese&#x20;

• Bengali&#x20;

• Bodo&#x20;

• Dogri&#x20;

• English&#x20;

• Gujarati&#x20;

• Hindi&#x20;

• Kannada&#x20;

• Kashmiri&#x20;

• Konkani&#x20;

• Maithili&#x20;

• Malayalam&#x20;

• Manipuri&#x20;

• Marathi&#x20;

• Nepali&#x20;

• Oriya&#x20;

• Punjabi&#x20;

• Sanskrit&#x20;

• Santali&#x20;

• Sindhi&#x20;

• Tamil&#x20;

• Telugu&#x20;

• Urdu

For serviceId as "\*\*bhashini/iiiith/indic-lang-detection-all\*\*", below are the supported languages-

• Assamese&#x20;

• Bengali&#x20;

• English&#x20;

• Gujarati&#x20;

• Hindi&#x20;

• Kannada&#x20;

• Malayalam&#x20;

• Manipuri&#x20;

• Marathi&#x20;

• Oriya&#x20;

• Punjabi&#x20;

• Tamil&#x20;

• Telugu&#x20;

• Urdu
{% endtab %}
{% endtabs %}

### Parameter: \`inputData\`

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input via \*\*source\*\* parameter .<br>

{% hint style="info" %}
input text content can be added as a value for \*\*source\*\* paramater under \*\*inputData\*\* complex tag
{% endhint %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/request-payload.md).

# Request Payload

This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.

## Request Payload for Transliteration Task

{% tabs %}
{% tab title="Transliteration" %}
{% code lineNumbers="true" %}

\`\`\`json

{
    "pipelineTasks": \[\
        {\
            "taskType": "transliteration",\
            "config": {\
                "language": {\
                    "sourceLanguage": "en",\
                    "targetLanguage": "hi"\
                },\
                "serviceId": "{{trans\_service\_id}}",\
                "isSentence": false,\
                "numSuggestions": 7\
            }\
        }\
    \],
    "inputData": {
        "input": \[\
            {\
                "source": "ki"\
            }\
        \]
    }
}

\`\`\`

{% endcode %}

This response contains 2 major parameters listed below and detailed further down the section:

1. pipelineTasks
2. inputData

### Parameter: \`pipelineTasks\`

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. \\
In the above example, \*\*\`pipelineTasks\`\*\* takes only one dictionary (line 3-13) because integrator wants to do only ASR.\\
\\
\*\*\`taskType\`\*\* parameter takes \`String\` that takes the value \*\*\`asr\`\*\*

\*\*\`config\`\*\* parameter takes a \*\*\`Dictionary\`\*\* that contains following parameters:

{% tabs %}
{% tab title="Language" %}
For ASR, \*\*\`language\`\*\* parameter only takes \*\*\`sourceLanguage\`\*\* which accepts \[ISO-639 Series Code\](/bhashini-apis/overall-understanding-of-the-api-calls.md) of the language.
{% endtab %}

{% tab title="Service ID" %}
serviceId parameter is obtained from the \[Transliteration Config Call\](/bhashini-apis/transliteration-config-call.md) \[response\](/bhashini-apis/pipeline-config-call/response-payload.md) as described \[here\](/bhashini-apis/transliteration-config-call/response-payload.md).
{% endtab %}

{% tab title="isSentence" %}
isSentence set to true and false for getting response in sentence.&#x20;
{% endtab %}

{% tab title="numSuggestions" %}
In the given request, the "numSuggestions" parameter is used in the "transliteration" task configuration. It is used to specify the number of transliteration suggestions that the task should provide.
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Parameters other than \*\*\`taskType\`\*\*, \*\*\`serviceId\`\*\* and \*\*\`config\`\*\* are optional.
{% endhint %}

### Parameter: \`inputData\`

inputData Parameter takes the actual input from the integrator on which the individual task has to be done. It can take the input either via \*\*\`input\`\*\* parameter .<br>

\* \*\*\`input\`\*\* parameter takes the text in source key

{% endtab %}
{% endtabs %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call.md).

# Text Language Detection Compute Call

This page will help the integrator to identify the language in an input texts. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.

\*\*Endpoint:\*\* \[\*\*https://dhruva-api.bhashini.gov.in/services/inference/pipeline\*\*\](https://dhruva-api.bhashini.gov.in/services/inference/pipeline)

\*\*Additional Headers:\*\*

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.

\* Accept: \\\*/\\\*
\* Authorization: INSERT\\\_API\\\_KEY\\\_HERE
\* Content-Type: application/json

Authorization : it is a HTTP header which is used to authenticate the user and permission of the requester to use protected resources. Authorization key value can be obtained from the My Profile section under the App name -> inference API key value after logging in to Bhashini-Udyat.

Accept : it is a HTTP header which is used to specify the types of content they can process. This helps the server understand what kind of response to send back.

Content-Type : it is HTTP header which is used to indicate the media type of the resource being sent. This helps the user understand how to process the content.

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, \*\*Authorization, Accept\*\* and \*\*Content-Type\*\* are the additional parameters sent.

<figure><img src="https://1033188871-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnW4gyGo8w1tpCSG4RZwV%2Fuploads%2FJ4c9DFEpDwyc3PWE8ZIZ%2Fimage.png?alt=media&amp;token=07f55e8e-113e-44d2-939d-375581541124" alt=""><figcaption></figcaption></figure>

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/download-postman-collection.md).

# Download Postman Collection

This page helps the integrator to obtains the JSON of the Postman collection which can be download and imported in Postman.

Create Workspace and import Collection

In Postman, access the \*\*\`Workspaces\`\*\* drop-down menu and click on \*\*\`Create Workspace\`\*\*

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2F61Q9H3hRUXKcXEHCG29R%2Fimage.png?alt=media&#x26;token=17422622-fb70-49cf-9397-0b74e2c1551e" alt="" width="100%">

Fill out the details required and click \*\*\`Create Workspace\`\*\* Button.

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2FVr4nxsJ49fhMjbC4Gp4s%2Fimage.png?alt=media&#x26;token=a3d88765-b55f-4fc5-88a9-72355e5c7c92" alt="" width="100%">

Go to a browser window (preferable Chromium based), and open the below URL:

{% hint style="info" %}
<https://api.postman.com/collections/33708049-43be070a-8630-44bf-8762-17e9551a3250?access\_key=PMAT-01K1WGWPRBYWSB89Q6TWCWJW21>
{% endhint %}

The webpage will show raw JSON content of the postman collection exposed via the above URL.

Follow the below steps to save this content to a JSON file:

1. Select all the content on the webpage.
2. Open a Notepad and paste the JSON content.
3. Save As this file and use the extension \\\[dot\] JSON to save the file as a JSON file type.
4. Choose the file name as per your requirement. e.g. collection
5. In the end, you will have \*\*\`collection.json\`\*\* file.

Goto Postman and click on \*\*\`import\`\*\* button towards the top left of the screen inside the workspace created above.

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2FTDNFZUBOljCMH0FyKMpP%2Fimage.png?alt=media&#x26;token=18a19e70-55e2-424e-9626-a0f5a0f9bcbb" alt="" width="100%">

In the box that appears, drag and drop the \*\*\`collection.json\`\*\* file created above.

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2FwSfJL2yzDU9muRCdwSOt%2Fimage.png?alt=media&#x26;token=f65066c1-581a-47e7-9fc8-cb91ae6a638c" alt="" width="100%">

Once imported, the collection will look something like below:

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2Fm2wc5UK5ev62eZVNik1h%2Fimage.png?alt=media&#x26;token=ce665816-7e34-470d-934c-935a47e5b8fb" alt="" width="100%">

{% hint style="info" %}
The collection is developed directly by Bhashini team and the same may change as per new changes that will be introduced over time.
{% endhint %}

## Accessing Variables

The postman collection has automation done for easy understanding of the integrators. For the same, variables are defined on Collection level.

To access these variables, click the \*\*\`Collection Name\`\*\* and then click on \*\*\`Variables\`\*\*.

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2FMor6mRsgBk9BhDN3XQAR%2Fimage.png?alt=media&#x26;token=c66958c1-ec0f-45f0-8e92-dcf1af10026e" alt="" width="100%">

This will list down all the variables that are used as a part of different API calls. Details of each variables is given below:

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2FJ0o9B9ZKiHcrXLP4dHbE%2Fimage.png?alt=media&#x26;token=b7ae2324-7c8d-4810-b83d-3c510ca03199" alt="" width="100%">

{% hint style="info" %}
These variables might change as and when new features will be avaiable as a part of different calls. The collection will have to be imported again to receive the updates.
{% endhint %}

\* \*\*\`ulca\_url:\`\*\* ULCA Endpoint to send the \[<mark style="color:orange;">Pipeline Config Call</mark>\](/bhashini-apis/pipeline-config-call.md)
\* \*\*\`user\_id:\`\*\* ID to uniquely identify each integrator as defined \[<mark style="color:orange;">here</mark>\](/bhashini-apis/pre-requisites-and-onboarding.md#obtaining-user-id).
\* \*\*\`api\_key:\`\*\* API Key as generated by the integrator for a specific application as described \[here\](/bhashini-apis/pre-requisites-and-onboarding.md#api-key-creation).
\* \*\*\`pipeline\_id:\`\*\* Pipeline ID obtained by the integrator either via discussion with Bhashini team, ULCA Web, or \[Pipeline Search Call\](/bhashini-apis/pipeline-search-call.md)
\* \*\*\`callback\_url:\`\*\* URL that is obtained from the response of \[Pipeline Config Call\](/bhashini-apis/pipeline-config-call.md) as described \[here\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineinferenceapiendpoint). This parameter is dynamically allocated with the value as discussed later in this page.
\* \*\*\`callback\_url\_feedback:\`\*\* Feedback URL that is obtained from the response of \[Pipeline Config Call\](/bhashini-apis/pipeline-config-call.md) as described \[here\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineinferenceapiendpoint). This parameter is dynamically allocated with the value as discussed later in this page.
\* \*\*\`compute\_call\_authorization\_key:\`\*\* This is a key parameter which is used for authorization of the \[Pipeline Compute Call\](/bhashini-apis/pipeline-compute-call.md) and is obtained from the response of \[Pipeline Config Call\](/bhashini-apis/pipeline-config-call.md) as described \[here\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineinferenceapiendpoint). This parameter is dynamically allocated with the value as discussed later in this page.
\* \*\*\`compute\_call\_authorization\_value:\`\*\* This is the value of the key above used for authorization of the \[Pipeline Compute Call\](/bhashini-apis/pipeline-compute-call.md) and is obtained from the response of \[Pipeline Config Call\](/bhashini-apis/pipeline-config-call.md) as described \[here\](/bhashini-apis/pipeline-config-call/response-payload.md#parameter-pipelineinferenceapiendpoint). This parameter is dynamically allocated with the value as discussed later in this page.
\* \*\*\`asr\_service\_id:\`\*\* ASR Service ID is the service ID allocated if \*\*ASR\*\* task is requested by the integrator either in individual task or as a combination of tasks and is dynamically allocated either via running \*\*\`With Config Request\`\*\* or \*\*\`Without Config Request\`\*\* as described in \[Request Payload\](/bhashini-apis/pipeline-config-call/request-payload.md).
\* \*\*\`nmt\_service\_id:\`\*\* NMT Service ID is the service ID allocated if \*\*Translation\*\* task is requested by the integrator either in individual task or as a combination of tasks and is dynamically allocated either via running \*\*\`With Config Request\`\*\* or \*\*\`Without Config Request\`\*\* as described in \[Request Payload\](/bhashini-apis/pipeline-config-call/request-payload.md).
\* \*\*\`tts\_service\_id:\`\*\* TTS Service ID is the service ID allocated if TTS task is requested by the integrator either in individual task or as a combination of tasks and is dynamically allocated either via running \*\*\`With Config Request\`\*\* or \*\*\`Without Config Request\`\*\* as described in \[Request Payload\](/bhashini-apis/pipeline-config-call/request-payload.md).
\* \*\*\`source\_language:\`\*\* Source Language takes in \[ISO 639 Series code\](/bhashini-apis/overall-understanding-of-the-api-calls.md) of the source language. Integrator defines this language so that the automation scripts written in Postman find appropriate Service IDs and allocated the \*\*\`asr\_service\_id\`\*\*, \*\*\`nmt\_service\_id\`\*\* and \*\*\`tts\_service\_id\`\*\*.
\* \*\*\`target\_language:\`\*\* Target Language takes in \[ISO 639 Series code\](/bhashini-apis/overall-understanding-of-the-api-calls.md) of the target language. Integrator defines this language so that the automation scripts written in Postman find appropriate Service IDs and allocated the \*\*\`asr\_service\_id\`\*\*, \*\*\`nmt\_service\_id\`\*\* and \*\*\`tts\_service\_id\`\*\*.
\* \*\*\`base64:\`\*\* This is an exemplary base64 content which is used for demo purposes. It can be replaced by the integrator as per their requirements.
\* \*\*\`inference\_input\_payload:\`\*\* This variable will be allocated with a value automatically after execution of the \*\*Postman Tests\*\* associated with and successful execution of \*\*\`Compute Request ASR\`\*\*. This is the input payload that is sent for making the \*\*\`Compute Request ASR\`\*\* API call. This variable will be used in \*\*\`Feedback Submission\`\*\* API Call. This is used for demo of Feedback Submission for \*\*ASR only\*\*. If any other Compute API call is made, developer should use the same input payload used for that particular Compute API which is then to be used for feedback submission.
\* \*\*\`inference\_output\_payload:\`\*\* This variable will be allocated with a value automatically after execution of the \*\*Postman Tests\*\* associated with and successful execution of \*\*\`Compute Request ASR\`\*\*. This is the output/response payload that is received after making a successful \*\*\`Compute Request ASR\`\*\* API call. This variable will be used in \*\*\`Feedback Submission\`\*\* API Call. This is used for demo of Feedback Submission for \*\*ASR only\*\*. If any other Compute API call is made, developer should use the same output/response payload received for that particular Compute API which is then to be used for feedback submission.
\* \*\*\`suggested\_inference\_output\_payload:\`\*\* This variable will have exact same structure as \*\*inference\\\_output\\\_payload\*\* along with the modified values. The concept is that developer is letting the sever know what should have been the response instead of what has currently being received. For ex. Developer send \*\*Compute Request NMT\*\* API call for doing a translation from \*\*English\*\* to \*\*Hindi\*\*. Developer receives a response which contains \*\*Hindi\*\* text somewhere in that response JSON, but the translated text is slightly incorrect. The incorrect part is corrected in the same place in the output response JSON and this new JSON (with edited and corrected \*\*Hindi\*\* text) is sent back to the server as a part of this variable.

### Accessing Automation Scripts <a href="#accessing-automation-scripts" id="accessing-automation-scripts"></a>

The Automation Scripts are written for \*\*\`With Config Request\`\*\* and \*\*\`Without Config Request\`\*\* API calls so that appropriate collection variables as described above can be allocated.

Once the Integrator clicks either of the API Call mentioned above, Automation Scripts can be accessed in the \*\*\`Tests Tab\`\*\* of that API Call as shown below:

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2F5NJCMTU9ODDQvbuU1fd6%2Fimage.png?alt=media&#x26;token=a2359dc8-6e21-4711-8895-6fd216668fa6" alt="Automation Script for Without Config Request API Cal" width="100%">

### Accessing Individual Calls and Combination Calls <a href="#accessing-individual-calls-and-combination-calls" id="accessing-individual-calls-and-combination-calls"></a>

<img src="https://709902406-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FSuLLfCr6CWwqT0SsqOL1%2Fuploads%2FH5L8TPt6CGsJtucdlvpx%2Fimage.png?alt=media&#x26;token=d6448b44-db8a-4dd2-a138-359177189832" alt="" width="100%">

Each individual as well as combination of tasks can be accessed easily.

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/request-payload.md).

# Request Payload

This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.

{% tabs %}
{% tab title="Speaker Diarization" %}

\`\`\`json
  {
    "pipelineTasks": \[\
        {\
            "taskType": "speaker-diarization",\
            "config": {\
                "serviceId": "{{speaker-diarization\_service\_id}}"\
            }\
        }\
    \],
    "inputData": {
        "audio": \[\
            {\
                "audioUri": "INSERT\_AUDIO\_URL\_HERE"\
              // "audioContent": "INSERT\_BASE64\_AUDIO\_HERE"    \
            }\
        \]
    }
}
\`\`\`

{% endtab %}
{% endtabs %}

This request contains 2 major parameters listed below and detailed further down the section:

1. pipelineTasks
2. inputData

\*\*Parameter: \`pipelineTasks\`\*\*

\*\*Type:\*\* Array

This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. In the above example, \*\*\`pipelineTasks\`\*\* takes only one dictionary (line 2-9) because integrator wants to do only Audio language detection. \*\*\`taskType\`\*\* parameter takes \`String\` that takes the value \*\*speaker-diarization.\*\*

\*\*\`config\`\*\* is a single key parameter which maps to another object called \*\*serviceId\*\*

The \*\*\`serviceId\`\*\* parameter is essential for invoking the backend model endpoint for the specified \*\*taskType\*\* with its authentication key. For supported \*\*\`serviceId\`\*\* and \*\*languages\*\* of the Speaker Diarization service, please visit this link.

{% embed url="<https://dibd-bhashini.gitbook.io/bhashini-apis/available-models-for-usage>" %}
\*\*Explore Available serviceIds and supported languages\*\*
{% endembed %}

\*\*\`preProcessors\`\*\* is an optional parameter which helps in reducing the background noise and to improve the clarity of the speech signal. These preprocessing steps help in improving the overall performance of speaker diarization API by providing cleaner and more structured input for the core diarization model.

### Parameter: \`inputData\`

inputData Parameter takes the actual input from the integrator on which the individual task has to be done.  in this case, the input is taken via audioUri or audioContent (base64 format).

{% hint style="info" %}
either user can pass \*\*audioUri\*\* as input or \*\*audioContent\*\* as input.
{% endhint %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/text-language-detection-compute-call/response-payload.md).

# Response Payload

This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.

\*\*Complete payload\*\*

<details>

<summary>Text language Detection response</summary>

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineResponse": \[\
        {\
            "taskType": "txt-lang-detection",\
            "config": null,\
            "output": \[\
                {\
                    "source": "INPUT\_TEXT",\
                    "langPrediction": \[\
                        {\
                            "langCode": "LANGUAGE\_CODE",\
                            "scriptCode": "SCRIPT\_CODE",\
                            "langScore": "LANGUAGE\_SCORE"\
                        }\
                    \]\
                }\
            \],\
            "audio": null\
        }\
    \]
}

\`\`\`

{% endcode %}

</details>

The above JSON Response shows the output of the Text language detection task requested by the integrator in that order.&#x20;

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/request-payload.md).

# Request Payload

This sub-page helps the integrator to understand various different types of request payload based on the individual task or combination of tasks in that sequence that integrator wants to do.

{% tabs %}
{% tab title="Audio language detection" %}
{% code overflow="wrap" lineNumbers="true" %}

\`\`\`json
{ 
  "pipelineTasks": \[ \
      { \
        "taskType": "audio-lang-detection",\
        "config": {\
                  "serviceId": "{{ald\_service\_id}}"\
                  } \
      }\
\],
"inputData": {
    "audio": \[\
        {\
            "audioContent": "INSERT\_BASE64\_AUDIO\_HERE"\
          //"audioUri": "INSERT\_AUDIO\_URL\_HERE"\
        }\
    \]
}
}

\`\`\`

{% endcode %}
{% endtab %}
{% endtabs %}

This request contains 2 major parameters listed below and detailed further down the section:

1. pipelineTasks
2. inputData

### Parameter: \`pipelineTasks\`

\*\*Type:\*\* Array\\
\\
This parameter takes an array of tasks, in the form of dictionary of \*\*\`taskType\`\*\* and \*\*\`config\`\*\*, that are to be done by the integrator. \\
In the above example, \*\*\`pipelineTasks\`\*\* takes only one dictionary (line 2-9) because integrator wants to do only Audio language detection.\\
\\
\*\*\`taskType\`\*\* parameter takes \`String\` that takes the value \*\*audio-lang-detection\*\*

\*\*\`config\`\*\* is a single key parameter which maps to another object called \*\*serviceId\*\*

{% tabs %}
{% tab title="serviceId" %}
serviceId parameter identifies the specific service/trained model you want to use.

For serviceId as "\*\*bhashini/iitmandi/audio-lang-detection/gpu\*\*", below are the supported languages-

\* Assamese
\* Bengali
\* English
\* Hindi
\* Kannada
\* Gujarati
\* Malayalam
\* Marathi
\* Odia
\* Punjabi
\* Tamil
\* Telugu
  {% endtab %}
  {% endtabs %}

### Parameter: \`inputData\`

inputData Parameter takes the actual input from the integrator on which the individual task has to be done.  in this case, the input is taken via audioUri or audioContent (base64 format).<br>

{% hint style="info" %}
either user can pass \*\*audioUri\*\* as input or \*\*audioContent\*\* as input.
{% endhint %}

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call.md).

# Audio Language Detection Compute Call

This page will help the integrator to identify the language spoken in an audio recording. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads.

\*\*Endpoint:\*\* \[\*\*https://dhruva-api.bhashini.gov.in/services/inference/pipeline\*\*\](https://dhruva-api.bhashini.gov.in/services/inference/pipeline)

\*\*Additional Headers:\*\*

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.

\* Accept: \\\*/\\\*
\* Authorization: INSERT\\\_API\\\_KEY\\\_HERE
\* Content-Type: application/json

Authorization : it is a HTTP header which is used to authenticate the user and permission of the requester to use protected resources. Authorization key value can be obtained from the My Profile section under the App name -> inference API key value after logging in to Bhashini-Udyat.

Accept : it is a HTTP header which is used to specify the types of content they can process. This helps the server understand what kind of response to send back.

Content-Type : it is HTTP header which is used to indicate the media type of the resource being sent. This helps the user understand how to process the content.

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, \*\*Authorization, Accept\*\* and \*\*Content-Type\*\* are the additional parameters sent.

<figure><img src="https://1033188871-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnW4gyGo8w1tpCSG4RZwV%2Fuploads%2F6bcKUI8bbbJPXp5GhAjy%2Fimage.png?alt=media&amp;token=d3e386b4-7a75-4595-8713-fa5498ee5530" alt=""><figcaption></figcaption></figure>

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-compute-call/response-payload.md).

# Response Payload

This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.

## Complete Payload

<details>

<summary>Transliteration</summary>

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineResponse": \[\
        {\
            "taskType": "transliteration",\
            "config": null,\
            "output": \[\
                {\
                    "source": "ki",\
                    "target": \[\
                        "की",\
                        "कि",\
                        "काई",\
                        "कीई",\
                        "काइ",\
                        "कीइ",\
                        "कै"\
                    \]\
                }\
            \],\
            "audio": null\
        }\
    \]
}
\`\`\`

{% endcode %}

</details>

The above JSON Response shows the output of the Transliteration task requested by the integrator in that order. Below we will discuss the individual task response as well as combination of tasks in specific sequence.

##

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/possible-errors.md).

# Possible Errors

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call.md).

# Speaker Diarization Compute Call

This page will help the integrator to identify the list of speakers spoken in an audio recording. This page will detail out the API call, its parameters, understanding of the Input and Output Payloads

\*\*Endpoint:\*\* \[\*\*https://dhruva-api.bhashini.gov.in/services/inference/pipeline\*\*\](https://dhruva-api.bhashini.gov.in/services/inference/pipeline)

\*\*Additional Headers:\*\*

Below is the understanding and process of obtaining the additional Headers that shall be sent to make the Pipeline Config API Call. These headers are used for uniquely identifying each integrator for a particular application and authenticate them for the API usage.

\* Accept: \\\*/\\\*
\* Authorization: INSERT\\\_API\\\_KEY\\\_HERE
\* Content-Type: application/json

Authorization : it is a HTTP header which is used to authenticate the user and permission of the requester to use protected resources. Authorization key value can be obtained from the My Profile section under the App name -> inference API key value after logging in to Bhashini-Udyat.

Accept : it is a HTTP header which is used to specify the types of content they can process. This helps the server understand what kind of response to send back.

Content-Type : it is HTTP header which is used to indicate the media type of the resource being sent. This helps the user understand how to process the content.

Below is a screenshot from the Postman. Along with standard headers that are sent automatically, \*\*Authorization, Accept\*\* and \*\*Content-Type\*\* are the additional parameters sent.

<figure><img src="https://1033188871-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnW4gyGo8w1tpCSG4RZwV%2Fuploads%2FKTz7GwBS9bT4VqKvEpab%2Fimage.png?alt=media&amp;token=76c2b414-5036-4fbb-9a54-badf9d1903a3" alt=""><figcaption></figcaption></figure>

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/appendix.md).

# Appendix

### Full Forms <a href="#full-forms" id="full-forms"></a>

ULCA: Universal Language Contribution APIs

ASR: Automatic Speech Recognition

NMT: Neural Machine Translation

TTS: Text to Speech

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/websocket-asr-api.md).

# WebSocket ASR API

### Overview

The \`ULCASocketClient\` is a WebSocket client that enables real-time \*\*Speech-to-Text (ASR)\*\* processing using \*\*BHASHINI's WebSocket API\*\*. This allows audio captured from a microphone to be streamed to Bhashini’s ASR service and receive transcription results \*\*asynchronously\*\*.

\*\*\*

### Prerequisites

Before you begin, ensure you have:

\* Access to a microphone
\* Bhashini \*\*API Key\*\* and \*\*Service ID\*\*
\* Internet connectivity
\* Java Development Kit (JDK) 8 or higher
\* Maven project setup
\* Java libraries:
  \* \`socket.io-client\` for WebSocket connection
  \* \`org.json\` for JSON processing

\*\*\*

### Required Dependencies (Maven)

\`\`\`xml
xmlCopyEdit<dependencies>
    <!-- Socket.IO client -->
    <dependency>
        <groupId>io.socket</groupId>
        <artifactId>socket.io-client</artifactId>
        <version>2.1.0</version>
    </dependency>

    <!-- JSON library -->
    <dependency>
        <groupId>org.json</groupId>
        <artifactId>json</artifactId>
        <version>20220320</version>
    </dependency>
</dependencies>
\`\`\`

\*\*\*

### Key Components

1. \*\*WebSocket Connection\*\*: Connect to Bhashini ASR service.
2. \*\*Audio Capture\*\*: Access microphone and record audio.
3. \*\*Audio Streaming\*\*: Stream audio to the server.
4. \*\*Response Handling\*\*: Receive transcription results from the server.

\*\*\*

### Implementation Steps

#### 1. Initialize Client

\`\`\`java
javaCopyEditULCASocketClient client = new ULCASocketClient("YOUR\_WEBSOCKET\_SERVER\_URL", "YOUR\_API\_KEY");
\`\`\`

#### 2. Connect to Server

\`\`\`java
javaCopyEditclient.connect();
\`\`\`

#### 3. Configure ASR Task

\`\`\`java
javaCopyEditJSONObject asrTask = new JSONObject();
asrTask.put("taskType", "asr");

JSONObject asrConfig = new JSONObject();
asrConfig.put("serviceId", "YOUR\_SERVICE\_ID");

JSONObject asrLanguage = new JSONObject();
asrLanguage.put("sourceLanguage", "en");
asrConfig.put("language", asrLanguage);
asrConfig.put("samplingRate", 8000);
asrConfig.put("audioFormat", "wav");
asrConfig.put("encoding", JSONObject.NULL);

asrTask.put("config", asrConfig);
JSONArray taskSequenceArray = new JSONArray().put(asrTask);
\`\`\`

#### 4. Configure Streaming

\`\`\`java
javaCopyEditJSONObject streamingConfig = new JSONObject();
streamingConfig.put("responseFrequencyInSecs", 2.0);
streamingConfig.put("responseTaskSequenceDepth", 1);
\`\`\`

#### 5. Start Streaming

\`\`\`java
javaCopyEditclient.startStream(taskSequenceArray, streamingConfig);
\`\`\`

#### 6. Start Audio Streaming (VAD-enabled)

The client listens for the \`ready\` event and then starts audio capture:

\`\`\`java
javaCopyEditclient.startContinuousAudioStreamingWithVAD();
\`\`\`

#### 7. Stop and Disconnect

\`\`\`java
javaCopyEditclient.stop(true);
client.disconnect();
\`\`\`

\*\*\*

### &#x20;Configuration Parameters

#### WebSocket Connection

| Parameter   | Description                                               |
| ----------- | --------------------------------------------------------- |
| \`serverUrl\` | WebSocket server URL (\`wss://dhruva-api.bhashini.gov.in\`) |
| \`apiKey\`    | Your Bhashini API key                                     |

#### ASR Task Configuration

| Parameter        | Description                  |
| ---------------- | ---------------------------- |
| \`taskType\`       | Must be \`"asr"\`              |
| \`serviceId\`      | Specific ASR service ID      |
| \`sourceLanguage\` | Language code (e.g., \`"en"\`) |
| \`samplingRate\`   | Usually \`8000\` Hz            |
| \`audioFormat\`    | Format: \`"wav"\`              |
| \`encoding\`       | Optional, often \`null\`       |

#### Streaming Config

| Parameter                   | Description                         |
| --------------------------- | ----------------------------------- |
| \`responseFrequencyInSecs\`   | Frequency of intermediate responses |
| \`responseTaskSequenceDepth\` | Depth of task-level responses       |

\*\*\*

### &#x20;Audio Specifications

\* \*\*Sampling Rate\*\*: 8000 Hz
\* \*\*Bit Depth\*\*: 16-bit
\* \*\*Channels\*\*: Mono
\* \*\*Encoding\*\*: PCM signed

\*\*\*

### Voice Activity Detection (VAD)

VAD ensures only meaningful (spoken) audio is transmitted:

\* Captures audio in real-time
\* Identifies speech segments
\* Reduces unnecessary data transmission

\*\*\*

### API Reference

#### Constructor

\`\`\`java
javaCopyEditULCASocketClient(String serverUrl, String apiKey)
\`\`\`

#### Methods

| Method                                   | Description                              |
| ---------------------------------------- | ---------------------------------------- |
| \`connect()\`                              | Establish WebSocket connection           |
| \`startStream(...)\`                       | Begin audio streaming                    |
| \`stop(boolean)\`                          | Stop the stream                          |
| \`disconnect()\`                           | Disconnect from server                   |
| \`startContinuousAudioStreamingWithVAD()\` | Start mic with VAD                       |
| \`convertByteToInt16(byte\[\])\`             | Convert byte array to 16-bit short array |
| \`toUnsignedBytes(short\[\])\`               | Convert short array to unsigned bytes    |

\*\*\*

### WebSocket Events

| Event        | Trigger                      |
| ------------ | ---------------------------- |
| \`connect\`    | Connection successful        |
| \`disconnect\` | Disconnected                 |
| \`ready\`      | Server is ready to receive   |
| \`response\`   | ASR result received          |
| \`message\`    | General server message       |
| \`abort\`      | Server aborted task          |
| \`terminate\`  | Server terminated connection |

\*\*\*

### &#x20;Complete Example

\`\`\`java
javaCopyEditpublic static void main(String\[\] args) {
    try {
        ULCASocketClient client = new ULCASocketClient("YOUR\_WS\_URL", "YOUR\_API\_KEY");
        client.connect();

        // ASR task config
        JSONObject asrTask = new JSONObject();
        asrTask.put("taskType", "asr");

        JSONObject config = new JSONObject();
        config.put("serviceId", "YOUR\_SERVICE\_ID");
        config.put("language", new JSONObject().put("sourceLanguage", "en"));
        config.put("samplingRate", 8000);
        config.put("audioFormat", "wav");
        config.put("encoding", JSONObject.NULL);
        asrTask.put("config", config);

        JSONArray taskSequence = new JSONArray().put(asrTask);

        // Streaming config
        JSONObject streamConfig = new JSONObject();
        streamConfig.put("responseFrequencyInSecs", 2.0);
        streamConfig.put("responseTaskSequenceDepth", 1);

        client.startStream(taskSequence, streamConfig);

        System.out.println("Streaming started. Press Enter to stop...");
        System.in.read();

        client.stop(true);
        client.disconnect();

    } catch (Exception e) {
        e.printStackTrace();
    }
}
\`\`\`

\*\*\*

### &#x20;Troubleshooting

#### &#x20;Connection Issues

\* Check \`serverUrl\`
\* Validate your API key
\* Ensure internet access

#### &#x20;No ASR Output

\* Confirm \`serviceId\`
\* Check audio format (wav, 8000 Hz)
\* Speak clearly/loud enough for VAD

#### Debugging Tips

\* Use console logs
\* Add \`System.out.println\` in event handlers
\* Watch server \`response\` events for error codes

\*\*\*

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/ocr-modalities-overview.md).

# OCR Modalities Overview

Optical Character Recognition (OCR) technologies are designed to process and interpret text from various input images. Depending on the nature of the input, OCR can be classified into 3 categories.

<details>

<summary>Printed OCR</summary>

This modality is optimized for processing printed documents, typically consisting of structured text in black ink on a white background. These documents are often plain and well-formatted, such as reports, books, or official records. The printed OCR modality is highly efficient at recognizing standard fonts and layouts, making it ideal for digitizing traditional printed materials. Sample image as below.

&#x20;                                                 !\[\](https://1033188871-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnW4gyGo8w1tpCSG4RZwV%2Fuploads%2F2xOnkDMChSldleAm1W11%2Fimage.png?alt=media\\&token=cfc9e157-e6c3-45e9-8073-6185e3ad5f6c)

</details>

<details>

<summary>Scenic OCR</summary>

Scenic OCR is designed to interpret text present in images that include natural or artificial scenes. These input images often combine visual elements such as landscapes, buildings, or objects with overlaid or embedded text. Scenic OCR is particularly useful for applications such as extracting text from signboards, advertisements, or product packaging, where the background and text are not standardized. Sample image as below.

&#x20;                                                 !\[\](https://1033188871-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnW4gyGo8w1tpCSG4RZwV%2Fuploads%2FZw6AIRGhRx4MBm6Aj0bM%2Fimage.png?alt=media\\&token=f778b023-a259-4ca6-a0ab-3967a67a32b3)

</details>

<details>

<summary>Handwritten OCR</summary>

This modality focuses on recognizing text from scanned images of handwritten documents. These inputs typically include variable writing styles, uneven spacing, and inconsistent text alignment. Handwritten OCR is essential for digitizing historical documents, handwritten forms, or personal notes. Advanced techniques in this modality aim to accommodate the diverse characteristics of handwriting to ensure accurate recognition. Sample image as below.

&#x20;                                                   !\[\](https://1033188871-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FnW4gyGo8w1tpCSG4RZwV%2Fuploads%2F9IITC7jH6mNWN1kjpyNQ%2Fimage.png?alt=media\\&token=2692e620-96cb-4513-a7da-f2b549793e3b)

</details>

Each modality addresses distinct challenges associated with input image types, enabling comprehensive OCR solutions for a wide range of use cases.

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/optical-character-recognition-call/response-payload.md).

# Response Payload

This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.

<details>

<summary>Optical Character Recognition Response</summary>

\`\`\`
{
    "pipelineResponse": \[\
        {\
            "taskType": "ocr",\
            "config": null,\
            "output": \[\
                {\
                    "source": "IMAGE\_TEXT\_CONTENT",\
                    "target": ""\
                }\
            \],\
            "audio": null\
        }\
    \]
}
\`\`\`

</details>

The above JSON Response shows the output of the Optical Character Recognition task requested by the integrator in that order.

#### Parameter: output <a href="#parameter-pipelinetasks" id="parameter-pipelinetasks"></a>

\*\*Type:\*\* Array

This parameter takes an array of tasks, in the form of dictionary of \*\*\`source and\`\*\* \*\*\`target\`\*\* that are to be done by the integrator. In the above example, \*\*\`output\`\*\* takes only one dictionary (line 6-11) in which \*\*\`output.source\`\*\* is a parameter which maps to output text content for the provided input image.

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/audio-language-detection-compute-call/response-payload.md).

# Response Payload

This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.

\*\*Complete Payload\*\*

<details>

<summary>Audio Language Detection response</summary>

{% code lineNumbers="true" %}

\`\`\`json
{
    "pipelineResponse": \[\
        {\
            "taskType": "audio-lang-detection",\
            "config": null,\
            "output": \[\
                {\
                    "audio": {\
                        "audioContent": "INPUT\_AUDIO\_CONTENT",\
                        "audioUri": null\
                    },\
                    "langPrediction": \[\
                        {\
                            "langCode": "LANGUAGE\_CODE",\
                            "scriptCode": null,\
                            "langScore": null\
                        }\
                    \]\
                }\
            \],\
            "audio": null\
        }\
    \]
}

\`\`\`

{% endcode %}

</details>

The above JSON Response shows the output of the Audio language detection task requested by the integrator in that order.&#x20;

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/speaker-diarization-compute-call/response-payload.md).

# Response Payload

This sub-page lets the integrator to actually be able to obtain the inference response with the output of individual tasks or tasks sequence in the order requested by the integrator.

\*\*Complete payload\*\*

<details>

<summary>Speaker Diarization response</summary>

\`\`\`json
{
    "taskType": "speaker-diarization",
    "output": \[\
        {\
            "speaker\_labels": \[\
                {\
                    "speaker1": \[\
                        {\
                            "start\_time": 5.44,\
                            "duration": 1.58\
                        }\
                    \]\
                }\
            \]\
        }\
    \]
}
\`\`\`

</details>

The above JSON Response shows the output of the Speaker Diarization task requested by the integrator in that order.&#x20;

---

# Unknown

\> For the complete documentation index, see \[llms.txt\](https://dibd-bhashini.gitbook.io/bhashini-apis/llms.txt). Markdown versions of documentation pages are available by appending \`.md\` to page URLs; this page is available as \[Markdown\](https://dibd-bhashini.gitbook.io/bhashini-apis/transliteration-config-call/response-payload.md).

# Response Payload

{% tabs %}
{% tab title="Request sent without configuration parameter" %}

## Complete Payload

<details>

<summary>Complete Payload</summary>

{% code lineNumbers="true" %}

\`\`\`json
{
  "languages": \[\
    {\
      "sourceLanguage": "en",\
      "targetLanguageList": \[\
        "as",\
        "bn",\
        "brx",\
        "gom",\
        "gu",\
        "hi",\
        "kn",\
        "ks",\
        "mai",\
        "ml",\
        "mni",\
        "mr",\
        "ne",\
        "or",\
        "pa",\
        "sa",\
        "sd",\
        "si",\
        "ta",\
        "te",\
        "ur"\
      \]\
    },\
    {\
      "sourceLanguage": "as",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "bn",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "brx",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "gom",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "gu",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "hi",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "kn",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ks",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "mai",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ml",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "mni",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "mr",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ne",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "or",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "pa",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "sa",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "sd",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "si",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ta",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "te",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ur",\
      "targetLanguageList": \[\
        "en"\
      \]\
    }\
  \],
  "pipelineResponseConfig": \[\
    {\
      "taskType": "transliteration",\
      "config": \[\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b0426e74a1c96b489b5441",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "as"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c7c97d6da5111fca0f5e4",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "bn"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b0427878d51611abf708c4",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "brx"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b3c64fa65d5a242f462655",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "gom"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c7c7d2abd9b3200b3003b",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "gu"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c73ce41dcd012c08f07e3",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "hi"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c7e662abd9b3200b3003c",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "kn"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b0429574a1c96b489b5442",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ks"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628cafad2abd9b3200b3003f",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "mai"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628ca83c2abd9b3200b3003e",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ml"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b0429f78d51611abf708c5",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "mni"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c811dd6da5111fca0f5e5",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "mr"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b042a878d51611abf708c6",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ne"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b042b878d51611abf708c7",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "or"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628ca0c52abd9b3200b3003d",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "pa"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b042c374a1c96b489b5443",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "sa"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628cab0ed6da5111fca0f5e8",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "sd"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628cad21d6da5111fca0f5e9",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "si"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c741941dcd012c08f07e4",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ta"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628ca307d6da5111fca0f5e6",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "te"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628ca3e8d6da5111fca0f5e7",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ur"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e599dd811234cfe86bb",\
          "language": {\
            "sourceLanguage": "as",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513eae9dd811234cfe86c3",\
          "language": {\
            "sourceLanguage": "bn",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e949dd811234cfe86c1",\
          "language": {\
            "sourceLanguage": "brx",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e3d9dd811234cfe86b8",\
          "language": {\
            "sourceLanguage": "gom",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513eb5610f2c0e43eeb476",\
          "language": {\
            "sourceLanguage": "gu",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513d39610f2c0e43eeb46e",\
          "language": {\
            "sourceLanguage": "hi",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e7d9dd811234cfe86c0",\
          "language": {\
            "sourceLanguage": "kn",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e4e610f2c0e43eeb471",\
          "language": {\
            "sourceLanguage": "ks",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e6c9dd811234cfe86be",\
          "language": {\
            "sourceLanguage": "mai",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e549dd811234cfe86ba",\
          "language": {\
            "sourceLanguage": "ml",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e84610f2c0e43eeb473",\
          "language": {\
            "sourceLanguage": "mni",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e71610f2c0e43eeb472",\
          "language": {\
            "sourceLanguage": "mr",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e5f9dd811234cfe86bc",\
          "language": {\
            "sourceLanguage": "ne",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e779dd811234cfe86bf",\
          "language": {\
            "sourceLanguage": "or",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e659dd811234cfe86bd",\
          "language": {\
            "sourceLanguage": "pa",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e43610f2c0e43eeb470",\
          "language": {\
            "sourceLanguage": "sa",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e489dd811234cfe86b9",\
          "language": {\
            "sourceLanguage": "sd",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e9d9dd811234cfe86c2",\
          "language": {\
            "sourceLanguage": "si",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e36610f2c0e43eeb46f",\
          "language": {\
            "sourceLanguage": "ta",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513ea6610f2c0e43eeb475",\
          "language": {\
            "sourceLanguage": "te",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e8c610f2c0e43eeb474",\
          "language": {\
            "sourceLanguage": "ur",\
            "targetLanguage": "en"\
          }\
        }\
      \]\
    }\
  \],
  "feedbackUrl": "https://dhruva-api.bhashini.gov.in/services/feedback/submit",
  "pipelineInferenceAPIEndPoint": {
    "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
    "inferenceApiKey": {
      "name": "Authorization",
      "value": "gQNj-sTUJjdkac\_hsmJLRlj9DeJzO6Q2qzW5SrshxQAwU635MyHXyAajtExDykfZ"
    },
    "isMultilingualEnabled": true,
    "isSyncApi": true
  },
  "pipelineInferenceSocketEndPoint": {
    "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
    "inferenceApiKey": {
      "name": "Authorization",
      "value": "gQNj-sTUJjdkac\_hsmJLRlj9DeJzO6Q2qzW5SrshxQAwU635MyHXyAajtExDykfZ"
    },
    "isMultilingualEnabled": true,
    "isSyncApi": true
  }
}
\`\`\`

{% endcode %}

</details>

Complete Payload shows the JSON structure of the content that is received when Integrator makes a ULCA Config Call without any configuration details as detailed in \`Tab 1\` of \[\*\*Request Payload\*\*\](/bhashini-apis/transliteration-config-call/request-payload.md#without-configuration-parameters)\\
\\
This response contains 3 major parameters listed below and detailed further down the section:

1. \[languages\](#parameter-languages)
2. \[pipelineResponseConfig\](#parameter-pipelineresponseconfig)
3. \[pipelineInferenceAPIEndPoint\](#parameter-pipelineinferenceapiendpoint)

### Parameter: \`languages\`

This parameter helps integrator to know what languages are available that can be used for the requested pipeline tasks in that sequence.\\
\\
For example, consider scenarios where Integrator requests for either:

\* Individual Task i.e., Transliteration \[here\](/bhashini-apis/pipeline-config-call/request-payload.md#integrators-want-to-do-individual-tasks)

For Single Tasks, the understanding is straight-forward that the languages appearing in the response corresponds to that task. e.g.&#x20;

\* If the integrator wants to do \*\*\`only Transliteration\`\*\*, the languages appearing shows that Server can do \*\*\`Transliteration\`\*\*&#x69;n these languages. In this case, parameters \*\*\`sourceLanguage\`\*\* and \*\*\`targetLanguageList\`\*\* means that for the languages appearing in \*\*\`targetLanguageList\`\*\* are the ones in which Server can do translation FROM the language that appear in \*\*\`sourceLanguage\`\*\*.

Usual format of language for such cases is below:

<details>

<summary>Supported Languages for requested Pipeline.</summary>

{% code lineNumbers="true" %}

\`\`\`json
"languages": \[\
    {\
      "sourceLanguage": "en",\
      "targetLanguageList": \[\
        "as",\
        "bn",\
        "brx",\
        "gom",\
        "gu",\
        "hi",\
        "kn",\
        "ks",\
        "mai",\
        "ml",\
        "mni",\
        "mr",\
        "ne",\
        "or",\
        "pa",\
        "sa",\
        "sd",\
        "si",\
        "ta",\
        "te",\
        "ur"\
      \]\
    },\
    {\
      "sourceLanguage": "as",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "bn",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "brx",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "gom",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "gu",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "hi",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "kn",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ks",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "mai",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ml",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "mni",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "mr",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ne",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "or",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "pa",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "sa",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "sd",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "si",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ta",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "te",\
      "targetLanguageList": \[\
        "en"\
      \]\
    },\
    {\
      "sourceLanguage": "ur",\
      "targetLanguageList": \[\
        "en"\
      \]\
    }\
  \]
\`\`\`

{% endcode %}

</details>

### Parameter: \`pipelineResponseConfig\`

This parameter helps the integrator to obtain the \*\*\`Service ID\`\*\* for a particular task type and language(s) associated with that task.

The task types appearing here will be the same as the ones that the integrator requested while sending the \*\*\`pipelineTasks\`\*\* parameter in \[Request Payload\](/bhashini-apis/transliteration-config-call/request-payload.md)\\
\\
\\
Say the language pair chosen is \*\*\`Bengali\`\*\* to \*\*\`Assamese\`\*\*.\\
\\
Integrator shall now obtain the Service ID correspondingly in the below manner:

1. Obtain Service ID for doing \*\*\`ASR\`\*\* in \*\*\`Bengali\`\*\*. Line 6 from Dictionary of Line 5-14 below.
2. Obtain Service ID for doing \*\*\`Translation\`\*\* from \*\*\`Bengali\`\*\* to \*\*\`Assamese\`\*\*. Line 49 from Dictionary of Line 48-55 below.
3. Obtain Service ID for doing \*\*\`TTS\`\*\* in \*\*\`Assamese\`\*\*. Line 89 from Dictionary of Line 88-98 below.

These Service IDs will be used in the \[Transliteration Compute Call.\](/bhashini-apis/transliteration-config-call.md)

{% hint style="info" %}
For each \*\*\`taskType\`\*\* in the response, there may appear additional configuration parameters that are specific to each \*\*\`taskType.\`\*\*

&#x20;
{% endhint %}

<details>

<summary>Configuration Details and Service IDs for requested pipeline tasks.</summary>

{% code lineNumbers="true" %}

\`\`\`json
"pipelineResponseConfig": \[\
    {\
      "taskType": "transliteration",\
      "config": \[\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b0426e74a1c96b489b5441",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "as"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c7c97d6da5111fca0f5e4",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "bn"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b0427878d51611abf708c4",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "brx"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b3c64fa65d5a242f462655",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "gom"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c7c7d2abd9b3200b3003b",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "gu"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c73ce41dcd012c08f07e3",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "hi"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c7e662abd9b3200b3003c",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "kn"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b0429574a1c96b489b5442",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ks"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628cafad2abd9b3200b3003f",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "mai"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628ca83c2abd9b3200b3003e",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ml"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b0429f78d51611abf708c5",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "mni"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c811dd6da5111fca0f5e5",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "mr"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b042a878d51611abf708c6",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ne"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b042b878d51611abf708c7",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "or"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628ca0c52abd9b3200b3003d",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "pa"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "62b042c374a1c96b489b5443",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "sa"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628cab0ed6da5111fca0f5e8",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "sd"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628cad21d6da5111fca0f5e9",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "si"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628c741941dcd012c08f07e4",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ta"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628ca307d6da5111fca0f5e6",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "te"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "628ca3e8d6da5111fca0f5e7",\
          "language": {\
            "sourceLanguage": "en",\
            "targetLanguage": "ur"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e599dd811234cfe86bb",\
          "language": {\
            "sourceLanguage": "as",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513eae9dd811234cfe86c3",\
          "language": {\
            "sourceLanguage": "bn",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e949dd811234cfe86c1",\
          "language": {\
            "sourceLanguage": "brx",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e3d9dd811234cfe86b8",\
          "language": {\
            "sourceLanguage": "gom",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513eb5610f2c0e43eeb476",\
          "language": {\
            "sourceLanguage": "gu",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513d39610f2c0e43eeb46e",\
          "language": {\
            "sourceLanguage": "hi",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e7d9dd811234cfe86c0",\
          "language": {\
            "sourceLanguage": "kn",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e4e610f2c0e43eeb471",\
          "language": {\
            "sourceLanguage": "ks",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e6c9dd811234cfe86be",\
          "language": {\
            "sourceLanguage": "mai",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e549dd811234cfe86ba",\
          "language": {\
            "sourceLanguage": "ml",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e84610f2c0e43eeb473",\
          "language": {\
            "sourceLanguage": "mni",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e71610f2c0e43eeb472",\
          "language": {\
            "sourceLanguage": "mr",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e5f9dd811234cfe86bc",\
          "language": {\
            "sourceLanguage": "ne",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e779dd811234cfe86bf",\
          "language": {\
            "sourceLanguage": "or",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e659dd811234cfe86bd",\
          "language": {\
            "sourceLanguage": "pa",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e43610f2c0e43eeb470",\
          "language": {\
            "sourceLanguage": "sa",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e489dd811234cfe86b9",\
          "language": {\
            "sourceLanguage": "sd",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e9d9dd811234cfe86c2",\
          "language": {\
            "sourceLanguage": "si",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e36610f2c0e43eeb46f",\
          "language": {\
            "sourceLanguage": "ta",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513ea6610f2c0e43eeb475",\
          "language": {\
            "sourceLanguage": "te",\
            "targetLanguage": "en"\
          }\
        },\
        {\
          "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
          "modelId": "63513e8c610f2c0e43eeb474",\
          "language": {\
            "sourceLanguage": "ur",\
            "targetLanguage": "en"\
          }\
        }\
      \]\
    }\
  \],
\`\`\`

{% endcode %}

</details>

### Parameter: \`pipelineInferenceAPIEndPoint\`

This parameter helps the integrator to know the details of the \[Transliteration Compute Call.\](/bhashini-apis/transliteration-config-call.md) where to send (\*\*\`callbackURL\`\*\* parameter) and shall be sent along with the \*\*\`Authorization Key-Value pair\`\*\* received under \*\*\`inferenceApiKey\`\*\* parameter which will be used for authentication of the same.

<details>

<summary>Details for Actual Inferencing.</summary>

{% code lineNumbers="true" %}

\`\`\`json
"pipelineInferenceAPIEndPoint": {
        "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
        "inferenceApiKey": {
            "name": "Authorization",
            "value": "cZVqccgm-LTAzxQVp6jjznmSR5RgKM"
        },
        "isMultilingualEnabled": true,
        "isSyncApi": true
    }
\`\`\`

{% endcode %}

</details>
{% endtab %}

{% tab title="Request sent with Configuration Parameter" %}

## Complete Payload

<details>

<summary>Complete Payload</summary>

{% code lineNumbers="true" %}

\`\`\`json
{
    "languages": \[\
        {\
            "sourceLanguage": "en",\
            "targetLanguageList": \[\
                "as",\
                "bn",\
                "brx",\
                "gom",\
                "gu",\
                "hi",\
                "kn",\
                "ks",\
                "mai",\
                "ml",\
                "mni",\
                "mr",\
                "ne",\
                "or",\
                "pa",\
                "sa",\
                "sd",\
                "si",\
                "ta",\
                "te",\
                "ur"\
            \]\
        }\
    \],
    "pipelineResponseConfig": \[\
        {\
            "taskType": "transliteration",\
            "config": \[\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "62b0426e74a1c96b489b5441",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "as"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628c7c97d6da5111fca0f5e4",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "bn"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "62b0427878d51611abf708c4",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "brx"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "62b3c64fa65d5a242f462655",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "gom"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628c7c7d2abd9b3200b3003b",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "gu"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628c73ce41dcd012c08f07e3",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "hi"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628c7e662abd9b3200b3003c",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "kn"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "62b0429574a1c96b489b5442",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "ks"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628cafad2abd9b3200b3003f",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "mai"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628ca83c2abd9b3200b3003e",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "ml"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "62b0429f78d51611abf708c5",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "mni"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628c811dd6da5111fca0f5e5",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "mr"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "62b042a878d51611abf708c6",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "ne"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "62b042b878d51611abf708c7",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "or"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628ca0c52abd9b3200b3003d",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "pa"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "62b042c374a1c96b489b5443",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "sa"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628cab0ed6da5111fca0f5e8",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "sd"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628cad21d6da5111fca0f5e9",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "si"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628c741941dcd012c08f07e4",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "ta"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628ca307d6da5111fca0f5e6",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "te"\
                    }\
                },\
                {\
                    "serviceId": "ai4bharat/indicxlit--cpu-fsv2",\
                    "modelId": "628ca3e8d6da5111fca0f5e7",\
                    "language": {\
                        "sourceLanguage": "en",\
                        "targetLanguage": "ur"\
                    }\
                }\
            \]\
        }\
    \],
    "feedbackUrl": "https://dhruva-api.bhashini.gov.in/services/feedback/submit",
    "pipelineInferenceAPIEndPoint": {
        "callbackUrl": "https://dhruva-api.bhashini.gov.in/services/inference/pipeline",
        "inferenceApiKey": {
            "name": "Authorization",
            "value": "gQNj-sTUJjdkac\_hsmJLRlj9DeJzO6Q2qzW5SrshxQAwU635MyHXyAajtExDykfZ"
        },
        "isMultilingualEnabled": true,
        "isSyncApi": true
    },
    "pipelineInferenceSocketEndPoint": {
        "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
        "inferenceApiKey": {
            "name": "Authorization",
            "value": "gQNj-sTUJjdkac\_hsmJLRlj9DeJzO6Q2qzW5SrshxQAwU635MyHXyAajtExDykfZ"
        },
        "isMultilingualEnabled": true,
        "isSyncApi": true
    }
}
\`\`\`

{% endcode %}

</details>

Complete Payload shows the JSON structure of the content that is received when Integrator makes a ULCA Config Call with some configuration details as detailed in \`Tab 2\` of \[Request Payload\](/bhashini-apis/transliteration-config-call/request-payload.md#with-configuration-parameters). Here, the integrator has requested to do a  tasks Transliteration in that sequence from \*\*\`English\`\*\*

### Parameter: \`languages\`

The understanding of the parameters remains same as in previous tab.\\
Since the languages were already known to the integrator before-hand, therefore, the response contains configuration details for those languages only.

{% hint style="info" %}
There may occur a possibility that Integrator wants to do any individual task or combination of tasks in a sequence for the languages that are \*\*\`not\`\*\* supported by that \*\*\`pipeline ID\`\*\* in which case the following response will be obtained:\\
\\
\*\*Response Code: 400 Bad Request\*\*\\
\*\*Response Body:\*\*

{% code lineNumbers="true" %}

\`\`\`json
{
    "code": "400 BAD\_REQUEST",
    "message": "Sequence of languages not supported",
    "timestamp": "2023-04-14T06:32:12.133+00:00"
}
\`\`\`

{% endcode %}

In such cases, it is recommended to send Pipeline Config Request without Configuration as shown in \`Tab 1\` under \[Request Payload\](/bhashini-apis/transliteration-config-call/request-payload.md#without-configuration-parameters)\\
Using which Integrators will know what all languages are supported by that pipeline ID.
{% endhint %}

### Parameter: \`pipelineResponseConfig\`

The understanding of the parameters remains same as in previous tab.\\
Since the languages were already known to the integrator before-hand, therefore, the response contains configuration details for those languages only.

### Parameter: \`pipelineInferenceAPIEndPoint\`

The understanding of the parameters remains same as in previous tab.
{% endtab %}
{% endtabs %}

---

