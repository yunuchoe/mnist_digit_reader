import React, { useState } from 'react';
import axios from 'axios';
import "./UploadFile.css"

const UploadFile: React.FC = () => {
  const [file, setFile] = useState<File|null>(null);
  const [result, setResult] = useState<{prediction: string; confidence: number} | null>(null);
  const [error, setError] = useState<string|null>(null);

  const handleFileChange = (change: React.ChangeEvent<HTMLInputElement>) => {
        if(change.target.files && change.target.files.length > 0){
            setFile(change.target.files[0]);
        }
  };

const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if(!file){
        setError('No file has been selected');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try{
        const response = await axios.post('/predict', formData, {headers:{'Content-Type': 'multipart/form-data'}, });
        setError(null);
        setResult(response.data);

        }catch(err: any){
            setError(err.response?.data?.error||'Caught error in uploading file');
            setResult(null);
        }
};

    return(
        <div className = "upload-file">
            <h1>MNIST Digit Predictor</h1>
            <form onSubmit = {handleSubmit}>
                <input type = "file" accept = "image/*" onChange = {handleFileChange}/>
                <button type = "submit">Predict</button>
            </form>

            {error && 
                <p style = {{color:'red'}}> {error} </p>
            }

            {result && (
                <div>
                <p>Predicted value: {result.prediction}</p>
                <p>Confidence percentage: {(result.confidence*100).toFixed(3)+"%"}</p>
                </div>
            )}
        </div>
        );

};

export default UploadFile;