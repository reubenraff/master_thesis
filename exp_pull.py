#!/usr/bin/env python
import argparse
import logging
import re
import trafilatura



def main(args):
    page_42 = [ "https://seekingalpha.com/article/4526497-integra-lifesciences-holdings-corporation-iart-ceo-jan-de-witte-on-q2-2022-results-earnings",
    "https://seekingalpha.com/article/4526495-owens-corning-oc-ceo-brian-chambers-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526494-hilton-worldwide-holdings-inc-hlt-ceo-chris-nassetta-on-q2-2022-results-earnings-call",
    "https://seekingalpha.com/article/4526493-edp-renovaveis-s-edrvf-ceo-miguel-andrade-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526492-konecranes-plc-kncrf-ceo-teo-ottola-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526491-waste-management-inc-wm-ceo-james-fish-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526487-nexans-s-s-nxprf-ceo-christopher-guerin-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526482-telefonica-brasil-s-viv-ceo-christian-gebara-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526481-premier-financial-corp-pfc-ceo-gary-small-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526480-loblaw-companies-limited-lblcf-ceo-galen-weston-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526478-first-quantum-minerals-ltd-fqvlf-ceo-tristan-pascall-on-q2-2022-results-earnings-call",
    "https://seekingalpha.com/article/4526476-veritex-holdings-inc-vbtx-ceo-malcolm-holland-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526474-ardmore-shipping-corporation-asc-ceo-anthony-gurnee-on-q2-2022-results-earnings-call",
    "https://seekingalpha.com/article/4526473-cargojet-inc-cgjtf-ceo-ajay-virmani-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526472-strategic-education-inc-s-stra-ceo-karl-mcdonnell-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526469-camtek-ltd-camt-ceo-rafi-amit-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526466-compan-de-minas-buenaventuras-bvn-ceo-leandro-garcia-on-q2-2022-results-earnings-call",
    "https://seekingalpha.com/article/4526464-group-1-automotive-inc-gpi-ceo-earl-hesterberg-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526462-crescent-point-energy-corp-cpg-ceo-craig-bryksa-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526461-option-care-health-inc-opch-ceo-john-rademacher-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526459-boston-properties-inc-bxp-ceo-owen-thomas-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526457-automatic-data-processing-adp-ceo-carlos-rodriguez-on-q4-2022-results-earnings-call",
    "https://seekingalpha.com/article/4526456-humana-inc-hum-ceo-bruce-broussard-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526455-first-bank-frba-ceo-patrick-ryan-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526452-cameco-corporation-ccj-ceo-timothy-gitzel-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526450-hess-corporation-hes-ceo-john-hess-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526447-monro-incs-mnro-ceo-michael-broderick-on-q1-2023-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526443-world-acceptance-corporations-wrld-ceo-chad-prashad-on-q1-2023-results-earnings-call",
    "https://seekingalpha.com/article/4526442-steven-madden-ltd-shoo-ceo-ed-rosenfeld-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526440-makemytrip-limited-mmyt-ceo-rajesh-magow-on-q1-2023-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526439-ameriprise-financial-inc-amp-ceo-jim-cracchiolo-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526437-kambi-group-plc-kmbif-ceo-kristian-nylen-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526436-cgi-inc-gib-ceo-george-schindler-on-q3-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526433-trustmark-corporation-trmk-ceo-duane-dewey-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526430-derma-sciences-inc-dsci-ceo-jan-de-witte-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526428-ashland-global-holdings-inc-ash-ceo-guillermo-novo-on-q3-2022-earnings-call-transcript",
    "https://seekingalpha.com/article/4526427-usana-health-sciences-usna-ceo-kevin-guest-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526425-jeronimo-martins-sgps-s-jronf-management-on-q2-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526424-te-connectivity-ltd-s-tel-ceo-terrence-curtin-on-q3-2022-results-earnings-call-transcript",
    "https://seekingalpha.com/article/4526422-lamb-weston-holdings-inc-lw-ceo-tom-werner-on-q4-2022-results-earnings-call-transcript"

    ]

    with open(args.file, "w+") as sink:
        for url in page_42:
            logging.warning(f"downloading {url}")
            downloaded = trafilatura.fetch_url(url) #'https://pubmed.ncbi.nlm.nih.gov/35675615/'
            #for content in downloaded:
            text = trafilatura.extract(downloaded)
            #logging.warning(f"writing {text}")
            print(text, file=sink)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument('url')
    parser.add_argument("file")
    main(parser.parse_args())


#19 383 934
