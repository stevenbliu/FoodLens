import React, { useState } from 'react';
import './App.css';
// import CryptoJS from 'crypto-js';  // Import crypto-js

const REACT_APP_NGROK_PUBLIC_URL = process.env.REACT_APP_NGROK_PUBLIC_URL;
const photo_url = `https://${REACT_APP_NGROK_PUBLIC_URL}/photos`;

function App() {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [foodInfo, setFoodInfo] = useState(null);
  const [fileName, setFileName] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile); // Track file for upload
      setFileName(selectedFile.name); // Update state with file name
    } else {
      setFile(null); // Clear file state if no file is selected
      setFileName(""); // Clear file name
    }
  };

  const handleImageUpload = async () => {
    if (!file) {
      alert("Please select an image.");
      return;
    }

    try {
      // Request presigned URL from the backend
      console.log(JSON.stringify({ filename: file.name, file_size: file.size }));
      const response = await fetch(`${photo_url}/create/`, {
        method: 'POST',
        body: JSON.stringify({ filename: file.name, file_size: file.size }),
        headers: { 'Content-Type': 'application/json' }
      });

      const jsonResponse = await response.json();

      // Check if the response has the URL and key
      if (!jsonResponse.url) {
        throw new Error("Invalid response from server");
      }

      console.log('Presigned URL obtained, starting image upload...');

      // Upload the image to S3 using the presigned URL
      const uploadResponse = await fetch(jsonResponse.url, {
        method: 'PUT',
        body: file,
        headers: {
          'Content-Type': file.type,
        }
      });

      if (uploadResponse.ok) {
        console.log('Upload successful');

        setImageUrl(`${jsonResponse.url}`);
        // fetchFoodInfo(jsonResponse.key);
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error("Error uploading image:", error);
      alert("Error uploading image: " + error.message);
    }
  };

  // const fetchFoodInfo = async (imageKey) => {
  //   try {
  //     const response = await fetch(`/identify-food/${imageKey}/`);
  //     const data = await response.json();

  //     if (data) {
  //       setFoodInfo(data);
  //     } else {
  //       alert("No food identified.");
  //     }
  //   } catch (error) {
  //     alert("Error identifying food: " + error.message);
  //   }
  // };

  const testButton = async () => {
    console.log('Test button pressed');
    try {
      const response = await fetch(`${photo_url}/upload-notification/`, { method: 'GET' });
      console.log(response.ok);
    } catch (error) {
      console.error('Error in testButton:', error);
    }
  };

  const subscribeView = async () => {
    console.log('Subscribe view button pressed');
    try {
      const response = await fetch(`${photo_url}/subscribe_view/`, { method: 'GET' });
      console.log(response.ok);
    } catch (error) {
      console.error('Error in subscribeView:', error);
    }
  };

  const snsEndpoint = async () => {
    console.log('SNS endpoint button pressed');
    try {
      const response = await fetch(`${photo_url}/sns_endpoint/`, { method: 'GET' });
      console.log(response.ok);
    } catch (error) {
      console.error('Error in snsEndpoint:', error);
    }
  };

  const uploadNotification = async () => {
    console.log('Upload notification button pressed');
    try {
      const response = await fetch(`${photo_url}/upload-notification/`, { method: 'GET' });
      console.log(response.ok);
    } catch (error) {
      console.error('Error in uploadNotification:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Food Identifier</h1>

        <div className="button-container">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="file-input"
          />
          {fileName && <p>Selected file: {fileName}</p>}

          <button onClick={handleImageUpload} className="upload-button">
            Upload Image
          </button>
          <button onClick={testButton} className="test-button">
            Test212312 Button
          </button>
          <button onClick={uploadNotification} className="upload-notification-button">
            Upload Notification Button
          </button>
          <button onClick={snsEndpoint} className="sns-endpoint-button">
            SNS Endpoint Button
          </button>
          <button onClick={subscribeView} className="subscribe-view-button">
            Subscribe View Button
          </button>
        </div>

        {/* Display the image if uploaded */}
        {imageUrl && <img src={imageUrl} alt="Uploaded preview" className="uploaded-image" />}
        
        {/* Display food information */}
        {foodInfo && (
          <div className="food-info">
            <h2>Food Info:</h2>
            <p><strong>Name:</strong> {foodInfo.name}</p>
            <p><strong>Description:</strong> {foodInfo.description}</p>
            {/* Add more food info fields as needed */}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
