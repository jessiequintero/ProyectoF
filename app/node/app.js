const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

// Resto de tu código aquí...


app.post('/configurar', (req, res) => {
  const { ip, usuario, contraseña } = req.body;

  // Llamar al script de Python con los datos recibidos
  const pythonProcess = spawn('python', ['script.py', ip, usuario, contraseña]);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Datos de salida del script de Python: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Error en el script de Python: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Proceso de Python cerrado con código ${code}`);
    res.json({ message: 'Configuración completada' });
  });
});

app.listen(port, () => {
  console.log(`Servidor Node.js escuchando en el puerto ${port}`);
});
