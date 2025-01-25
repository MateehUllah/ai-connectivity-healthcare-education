import axios from 'axios';

export const submitData = async (type, coordinates, formData) => {
  try {
    const payload = {
      Latitude: parseFloat(coordinates.lat),
      Longitude: parseFloat(coordinates.lng),
      ...formData
    };

    const response = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/predict/${type}`,
      payload
    );
    
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};