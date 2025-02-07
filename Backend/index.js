import express from 'express';
import cors from 'cors';
import ComandModel from './model/comand.js'
import mongoose from 'mongoose';


mongoose
    .connect('mongodb+srv://vladmorozov2020:Nevskifront208@moroz.gjylj0v.mongodb.net/Vibus_ML_278?retryWrites=true&w=majority&appName=Moroz')
    .then(() =>{console.log("DB OK")})
    .catch((err) => {console.log('DB ERR', err)})



const app = express();

app.use(express.json());
app.use(cors());



app.get("/", (req, res) => {
    res.send("<h2>Vibus-ML-278 Server is running</h2>");
});


app.post('/file', (req, res) => {
    const fileInfo = req.body;

    if (!fileInfo.file_name || !fileInfo.file_path) {
        return res.status(400).json({ message: 'Ошибка: file_name и file_path обязательны.' });
    }

    console.log('📥 Получены данные о файле:');
    console.log(`Имя файла: ${fileInfo.file_name}`);
    console.log(`Путь к файлу: ${fileInfo.file_path}`);

    res.status(200).json({ message: 'Данные о файле успешно получены.', data: fileInfo });
});

app.post('/disk', (req, res) => {
    const disks = req.body;

    if (!disks.disks || !Array.isArray(disks.disks)) {
        return res.status(400).json({ message: 'Ошибка: ожидается массив disks.' });
    }

    console.log('📥 Получены данные о дисках:');
    disks.disks.forEach((disk, index) => {
        console.log(`  [${index}] ${disk}`);
    });

    res.status(200).json({ message: 'Данные о дисках успешно получены.', data: disks });
});

app.post('/post', async (req, res) => {
    try{
  
     const doc = new ComandModel({
        comand: req.body.comand
     });


     const coman = await doc.save();
     
 
     res.json({
         ...coman._doc
     })}
    catch (err){
        res.status(500).json({
            message: 'неудалось сополучить команду'
        });
        console.log(err)
   }
    });
app.put('/zapr/:id', async (req, res) => {
    try {
        const comId = req.params.id;
        const commandd = await ComandModel.updateOne(
            {
                _id: comId
            },
            {
                comand: req.body.comand,
            }
        )
        res.json({
            sucses: true
        })
    }   
    catch (err){
        res.status(500).json({
            message: 'неудалось сополучить команду'
        });
        console.log(err)
   }
});

app.get('/zapr/:id', async (req, res) => {
    try {
        const postId = req.params.id;
        const commandd = await ComandModel.findById(postId)
    res.json(commandd)
    }   
    catch (err){
        res.status(500).json({
            message: 'неудалось сополучить статью'
        });
        console.log(err)
   }
});

app.post('/dirs', (req, res) => {
    const dirs = req.body;

    if (!dirs.directories || !Array.isArray(dirs.directories)) {
        return res.status(400).json({ message: 'Ошибка: ожидается массив directories.' });
    }

    console.log('📥 Получены данные о директориях:');
    dirs.directories.forEach((dir, index) => {
        console.log(`  [${index}] ${dir}`);
    });

    res.status(200).json({ message: 'Данные о директориях успешно получены.', data: dirs });
});

app.use((req, res) => {
    res.status(404).send('Ошибка 404: путь не найден.');
});







// Запуск сервера
const PORT = 5050;
app.listen(PORT, (err) => {
    if (err) {
        return console.error('Ошибка запуска сервера:', err);
    }
    console.log(` http://localhost:${PORT}`);
});