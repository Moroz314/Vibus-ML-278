import mongoose from "mongoose";

const Comand_Schema = new mongoose.Schema({
    comand: {
        type: String,
        default: "",
    }
    },
    {
        timestamps: true,
    }
);


export default mongoose.model('Command', Comand_Schema)