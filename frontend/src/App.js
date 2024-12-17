import React, { useState } from 'react';
import './App.css';

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

      const response = await fetch('http://localhost:8000/photo-handler/get-presigned-url/', {
        method: 'POST',
        body: JSON.stringify({ filename: file.name, file_size: file.size }),
        headers: { 'Content-Type': 'application/json' }
    });
      const jsonResponse = await response.json();
  
      // console.log(jsonResponse);  // Log the response to check its structure
      console.log(jsonResponse)

      // Check if the response has the URL and key
      // if (!jsonResponse.url || !jsonResponse.key) {
      //   throw new Error("Invalid response from server");
      // }
      console.log(response)
  
      // // Upload the image to S3 using the presigned URL
      // const uploadResponse = await fetch(jsonResponse.url, {
      //   method: 'PUT',
      //   body: file,
      // });
      // console.log('2')

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

  return (
    <div className="App">
      <header className="App-header">
        <h1>Food Identifier</h1>

        {/* Upload Form */}
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleImageUpload}>Upload Image</button>

        {/* Display Uploaded Image */}
        {imageUrl && <img src={imageUrl} alt="Uploaded Food" className="food-image" />}

        {/* Display Food Information */}
        {foodInfo && (
          <div className="food-info">
            <h2>{foodInfo.name}</h2>
            <p>{foodInfo.description}</p>
            <p><strong>Calories:</strong> {foodInfo.calories}</p>
            {/* Add other food details here */}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
