import express from 'express';
import cors from 'cors'


const app = express();

app.use(express.json());
 
app.use(cors());

app.get("/", function(request, response){

    response.send("<h2>Vibus-ML-278</h2>");

});


const PORT = 5050;

app.listen(PORT, (err) => {
    if(err){
   return console.log(err);
  }
  console.log('Server Ok')
})

