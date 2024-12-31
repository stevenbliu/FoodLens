import React, { useState } from 'react';
import './App.css';

const REACT_APP_NGROK_PUBLIC_URL = process.env.REACT_APP_NGROK_PUBLIC_URL;
const photo_url = `${REACT_APP_NGROK_PUBLIC_URL}/photos`;

function App() {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [foodInfo, setFoodInfo] = useState(null);
  const [fileName, setFileName] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile || null);
    setFileName(selectedFile ? selectedFile.name : '');
  };

  const fetchWithHeaders = async (url, options) => {
    const headers = {
      'Content-Type': 'application/json',
      'ngrok-skip-browser-warning': 63940,
    };
  
    const mergedOptions = { ...options, headers: { ...headers, ...options?.headers } };
  
    try {
      const response = await fetch(url, mergedOptions);
  
      if (!response.ok) {
        const responseText = await response.text();  // Log response body
        console.error('Response body:', responseText);
        throw new Error(`HTTP error! Status: ${response.status} - ${responseText}`);
      }
  
      return await response.json();
    } catch (error) {
      console.error('Error fetching data:', error);
      throw error;
    }
  };

  const handleImageUpload = async () => {
    if (!file) {
      alert('Please select an image.');
      return;
    }

    setIsUploading(true); // Set loading state to true

    try {
      const createResponse = await fetchWithHeaders(`${photo_url}/create/`, {
        method: 'POST',
        body: JSON.stringify({ filename: file.name, file_size: file.size }),
      });

      const { url } = await createResponse;
      if (!url) throw new Error('Invalid response from server.');

      const uploadResponse = await fetch(url, {
        method: 'PUT',
        body: file,
        headers: { 'Content-Type': file.type },
      });

      if (uploadResponse.ok) {
        setImageUrl(url);
        // alert('Image uploaded successfully!');
      } else {
        throw new Error('Image upload failed.');
      }
    } catch (error) {
      console.error('Error uploading image:', error);
      alert(`Error: ${error.message}`);
    } finally {
      setIsUploading(false); // Reset loading state
    }
  };

  const handleRequest = async (url, method = 'GET', data = null) => {
    const options = { 
      method, 
      headers: { 
        'Content-Type': 'application/json', 
      },
    };
  
    // Only add the body if the method is POST or PUT
    if (data && (method === 'POST' || method === 'PUT')) {
      options.body = JSON.stringify(data);
    }
  
    try {
      const response = await fetchWithHeaders(url, options);
      return response;
    } catch (error) {
      console.error(`Error during ${method} request:`, error);
    }
  };
  

  const sendTestRequest = () => handleRequest(`${photo_url}/inject-test-data/`, 'POST');
  const subscribeToNotifications = () => handleRequest(`${photo_url}/subscribe/`, 'GET');
  const fetchPhotoDetails = () => handleRequest(`${photo_url}/11/`, 'GET');

  const notifyUpload = (method = 'GET') => handleRequest(`${photo_url}/upload-notification/`, method);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Food Identifier</h1>

        <div className="button-container">
          <input type="file" accept="image/*" onChange={handleFileChange} className="file-input" />
          {fileName && <p>Selected file: {fileName}</p>}

          <button onClick={handleImageUpload} className="upload-button" disabled={isUploading}>
            {isUploading ? 'Uploading...' : 'Upload Image'}
          </button>
          <button onClick={sendTestRequest} className="test-button">Send Test Request</button>
          <button onClick={() => notifyUpload('GET')} className="upload-notification-button">Get Notification</button>
          <button onClick={() => notifyUpload('POST')} className="sns-endpoint-button">Post Notification</button>
          <button onClick={subscribeToNotifications} className="subscribe-view-button">Subscribe</button>
          <button onClick={fetchPhotoDetails} className="fetch-photo-button">Fetch Photo Details</button>
        </div>

        {imageUrl && <img src={imageUrl} alt="Uploaded preview" className="uploaded-image" />}

        {foodInfo && (
          <div className="food-info">
            <h2>Food Info:</h2>
            <p><strong>Name:</strong> {foodInfo.name}</p>
            <p><strong>Description:</strong> {foodInfo.description}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
