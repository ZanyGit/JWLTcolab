const axios = require('axios');
const url = 'https://api-extern.systembolaget.se/product/v1/product/1';
const urlAll = 'https://api-extern.systembolaget.se/product/v1/product';
const dinApiNyckel = 'DIN API NYCKEL'
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/myapp', {useNewUrlParser: true, useUnifiedTopology:true});


const varaSchema = new mongoose.Schema({
  namn: String,
  pris: Number,
  produktId: String
});

const Vara = mongoose.model('Vara',varaSchema);


const getItem = async () => {
  let res = await axios.get(url,{headers:{
    'Ocp-Apim-Subscription-Key':
    'd47a74584689413da488540a0e1f2b27'}
  })
  let {ProductId, ProductNameBold,Price} = res.data
  console.log(`PruductId: ${ProductId} Name: ${ProductNameBold} Price: ${Price}`)
}

const getAllItems = async () => {
  let res = await axios.get(urlAll,{headers:{
    'Ocp-Apim-Subscription-Key':
    'd47a74584689413da488540a0e1f2b27'}
  })
  console.log(`Antal varor: ${res.data.length}`)

  for(let element of res.data){
    Vara.findOne({produktId:element.ProductId},async function(err, result){
      if(err){
        console.log(err)
      }else{
        if(result){
          if(result.pris != element.Price){
            console.log(`${result.namn}, prisförändring: ${element.Price - result.pris}kr ${((element.Price - result.pris)/result.pris).toFixed(2)}% (updated)`)
            result.pris = element.Price
            await result.save()
          }

        }else{
          let newOne = new Vara({
            namn:element.ProductNameBold,
            pris:element.Price,
            produktId:element.ProductId});
          await newOne.save()
        }
      }
    });
  }
}

getAllItems()


// getItem()
// axios.get(url,{headers:{
//   'Ocp-Apim-Subscription-Key':
//   'd47a74584689413da488540a0e1f2b27'}
// }).then(function(res){
//   console.log(res.data)
// }).catch(function(err){
//   console.log(err)
// })
