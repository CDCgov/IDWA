import { ExtractStep } from "../utils/constants";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import ExtractDataHeader from "../components/ExtractDataHeader";
import React from "react";
import { ExtractStepper } from "../components/ExtractStepper";
import { Table, Icon, Button } from "@trussworks/react-uswds";
import { Divider } from "../components/Divider";
import documentImage from "./SyphForm.png"; //Please enter your file of choice here
import "./ReviewTemplate.scss";
import aiIconUrl from "../assets/ai_icon.svg";
import {SortableTable} from "../components/SortableTable/SortableTable.tsx";
import {EditableText} from "../components/EditableText/EditableText.tsx";

interface Result {
  text: string;
  confidence: number;
  edited?: boolean;
}

interface SubmissionData {
  template_name: string;
  file_image: string;
  results: {
    [key: string]: Result;
  };
}

const ReviewTemplate: React.FC = () => {
  const navigate = useNavigate();
  const [index, setIndex] = useState<number>(0);
  const [submissionData, setSubmissionData] = useState<SubmissionData | null>(
    null
  );

  const [images, setImages] = useState<string[]>([]);

  const fakeData = {
    template_name: "Syph Template",
    file_image: documentImage,
    results: {
      Name: {
        text: "TESTPATIENT,13",
        confidence: 97,
      },
      Patient_ID: {
        text: "12090546",
        confidence: 98,
      },
      DrawLocation: {
        text: "BH_1Diamondd_LAB",
        confidence: 56,
      },
    },
  };

  const handleImageChange = (index: number) => {
    setIndex(index);
  }
    
  useEffect(() => {
    const data = localStorage.getItem("submission");
    if (data) {
      setSubmissionData(JSON.parse(data));
    } else {
      // use fakedata if no data
      setSubmissionData(fakeData);
    }
  }, []);

  const [editedValues, setEditedValues] = useState<Map<string, string>>(new Map());

  useEffect(() => {
    const data = localStorage.getItem("images");
    if (data) {
      setImages(JSON.parse(data));
    } else {
      // use fakedata if no data
      setImages([documentImage]);
    }
  }, []);

  const handleBack = () => {
    navigate("/extract/upload");
  };

  const handleSubmit = () => {
    navigate("/extract/submit");
  };

  const handleClose = () => {
    navigate("/");
  };



  //fallback if no valid template is available can edit if needed
  if (!submissionData) {
    return <div>No submission Data</div>;
  }
  const { file_image, results } = submissionData;
  const confidenceVal = 75;

  const resultsTable = Object.entries(results).map(([k, v], idx) => {
    const overrideValue = editedValues[k]
    return {
      index: idx,
      name: k,
      value: overrideValue || v.text,
      confidence: overrideValue ? 100 : v.confidence,
      isError: overrideValue ? false : v.confidence <= confidenceVal,
      isEdited: !!overrideValue
    }
  });

  const calculateOverallConfidence = () => {
    if (!submissionData) return 0;
    const results = resultsTable;
    const totalConfidence = results.reduce((sum, result) => {
      return sum + result.confidence;
    }, 0);
    return (totalConfidence / results.length).toFixed(2);
  };

  const errorCount = resultsTable.filter(
      (r) => r.isError
  ).length;
  const hasErrors = errorCount > 0;
  const overallConfidence = calculateOverallConfidence();



  const isErrorFormatter = (d) => {
    return d ? <Icon.Warning className="text-error" /> : "";
  }

  const labelConfidenceFormatter = (d, _idx, row) => {
    return row.isEdited ? "Edited" : redTextOnErrorFormatter(`${d.toFixed(0)}%`, row.index, row)
  }

  const redTextOnErrorFormatter = (d, _idx, row) => {
    return row.isError ? <span className="text-error">{d}</span> : d;
  }

  const editCellFormatter = (d, _idx, row) => {
    return <EditableText dataTestId={`${row.isError ? 'edit-fix-error' : null}`} text={d} onSave={(value) => {
      setEditedValues({...editedValues, [row.name]: value})
    }} textFormatter={(s) => row.isError ? <span className="text-error">{s}</span> : s}/>
  }

  return (
      <div className="display-flex flex-column flex-justify-start width-full height-full padding-1 padding-top-2">
      <ExtractDataHeader
        onSubmit={handleSubmit}
        onExit={handleClose}
        onBack={handleBack}
        isUploadComplete={!hasErrors}
      />
      <Divider margin="0px" />
      <div className="display-flex flex-justify-center padding-top-4">
        <ExtractStepper currentStep={ExtractStep.Review} />
      </div>

      <div className="display-flex flex-justify-between padding-top-4">
        <div className="width-50">
          <div className="margin-top-2 margin-bottom-1">
            <div className="display-flex flex-align-center">
              <h3>Extracted Data</h3>
            </div>
            <div className="display-flex flex-align-center">
              <img src={aiIconUrl} alt="AI Icon" aria-hidden={true} />
              <span className="font-sans-md font-weight-semibold">
                <b> Overall confidence score (CS): </b>
                <span
                  className={`text-black margin-left-05 ${
                    Number(overallConfidence) < Number(confidenceVal)
                      ? "text-error"
                      : "text-success"
                  }`}
                >
                  {overallConfidence}%
                </span>
              </span>

              <div className="custom-tooltip-container">
                <Icon.Help aria-hidden={true} />
                <span className="custom-tooltip-text">
                  Overall Confidence Score is the average of all Individual
                  Confidence Scores.
                </span>
              </div>
            </div>
            <p className="font-sans">
              Review and edit errors before you submit.
            </p>
            <div className="display-flex flex-align-center text-error">
              {hasErrors && (
                <>
                  <span className="font-sans-sm margin-right-1">
                    Errors: {errorCount}
                  </span>
                  <Icon.Warning className="text-error" />
                </>
              )}
            </div>
          </div>

          <SortableTable
              columns={["name", "value", "isError", "confidence"]}
              data={resultsTable}
              sortableBy={["name", "confidence", "value"]}
              defaultSort={"confidence"}
              columnNames={{name: "Label", value: "Value", isError: " ", confidence: "Label Confidence"}}
              formatters={{isError: isErrorFormatter, confidence: labelConfidenceFormatter, value: editCellFormatter}}
            />

        </div>
        <div className="width-50">
          <div
            className="width-full bg-white border-gray-5 border-1px"
          >
            <div>
              {images.map((_, index) => (
                <Button key={index} onClick={() => handleImageChange(index)} type='button'>
                    Image {index + 1}
                </Button>
              ))}
            </div>
            {
              images.map((image, innerIndex) => (
                <img
                  key={`image-${innerIndex}`}
                  src={image}
                  alt={`Document ${innerIndex + 1}`}
                  style={{
                    width: "100%",
                    marginBottom: "20px",
                    display: index === innerIndex ? "block" : "none",
                  }}
                />
              ))
            }
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReviewTemplate;