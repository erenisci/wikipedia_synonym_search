
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method Not Allowed' });
  }

  const { word } = req.body;

  if (!word) {
    return res.status(400).json({ message: 'Kelime gerekli.' });
  }

  try {
    const response = await fetch('http://localhost:5000/find-synonyms', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ word }),
    });

    const data = await response.json();

    if (response.ok) {
      return res.status(200).json(data);
    } else {
      return res.status(response.status).json(data);
    }
  } catch (error) {
    return res.status(500).json({ message: 'Bir hata oluştu.' });
  }
}
