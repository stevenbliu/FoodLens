import React, { useState } from 'react';
import './App.css';

import CryptoJS from 'crypto-js';  // Import crypto-js

// Function to calculate the MD5 checksum
function calculateMD5(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = function (e) {
      // Create an array from the result and calculate MD5 hash
      const arrayBuffer = e.target.result;
      const wordArray = CryptoJS.lib.WordArray.create(arrayBuffer);
      
      // Calculate MD5 and return as Base64 string
      const md5 = CryptoJS.MD5(wordArray).toString(CryptoJS.enc.Base64);
      resolve(md5);
    };
    
    reader.onerror = reject;
    
    reader.readAsArrayBuffer(file); // Use readAsArrayBuffer instead of readAsBinaryString
  });
}

function App() {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [foodInfo, setFoodInfo] = useState(null);

  // Handle file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleImageUpload = async () => {
    if (!file) {
      alert("Please select an image.");
      return;
      console.log('1')

    }
    console.log('12')

    try {
      // Request presigned URL from the backend
      // const response = await fetch(`/photo-handler/generate-presigned-url/${file.name}/${file.size}/`);
      
      const md5Checksum = await calculateMD5(file);
      console.log('cheksum:', md5Checksum)

      console.log("Fetch requested")
      const response = await fetch('http://localhost:8000/photo-handler/get-presigned-url/', {
        method: 'POST',
        body: JSON.stringify({ filename: file.name, file_size: file.size, md5Checksum: md5Checksum }),
        headers: { 'Content-Type': 'application/json' }
    });

      const jsonResponse = await response.json();
  
      // console.log(jsonResponse);  // Log the response to check its structure
      console.log(jsonResponse)

      // Check if the response has the URL and key
      if (!jsonResponse.url) {
        throw new Error("Invalid response from server");
      }


      // return
      // return 
      console.log('Uploading image')
      // Upload the image to S3 using the presigned URL
      const uploadResponse = await fetch(jsonResponse.url, {
        method: 'PUT',
        body: file,
        headers:
        {
          'Content-Type': file.type,
          // 'Content-MD5': md5Checksum, 
        }
      });
      // Handle the response
      if (!uploadResponse.ok) {
        console.error('Upload failed:', uploadResponse.status, uploadResponse.statusText);
        const errorResponse = await uploadResponse.text();
        console.error('Error response:', errorResponse);
      } else {
        console.log('Upload successful');
  }

      // if (uploadResponse.ok) {
      //   // After upload, display the uploaded image and send a request to identify the food
      //   setImageUrl(`https://your-s3-bucket-url/${jsonResponse.key}`);
      //   fetchFoodInfo(jsonResponse.key);
      // } else {
      //   throw new Error("Image upload failed");
      // }
    } catch (error) {
      alert("Error uploading image: " + error.message);
    }
  };

  // Fetch food information from backend
  const fetchFoodInfo = async (imageKey) => {
    try {
      // Call your backend to identify the food (you can modify the endpoint as needed)
      const response = await fetch(`/identify-food/${imageKey}/`);
      const data = await response.json();

      if (data) {
        setFoodInfo(data);
      } else {
        alert("No food identified.");
      }
    } catch (error) {
      alert("Error identifying food: " + error.message);
    }
  };

  const testButton = async () => {
    console.log('test buttoning...')
    const response = await fetch('http://localhost:8000/photo-handler/upload-notification/', {
      method: 'GET',
  });
    console.log(response.ok)
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Food Identifier</h1>

        <div className="button-container">
        <input type="file" accept="image/*" onChange={handleFileChange} className="file-input" />
        <button onClick={handleImageUpload} className="upload-button">Upload Image</button>
        <button onClick={testButton} className="test-button">Test Button</button>
        </div>

      </header>
    </div>
  );
}

export default App;
