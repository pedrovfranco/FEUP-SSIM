const mongoose = require('mongoose');

const rewardsSchema = new mongoose.Schema(
    {
        name: {
            type: String,
            required: true
        },
        costRewardsPoints: {
            type: Number,
            required: true
        },
        numberOfRewards: {
            type: Number,
            required: true
        },
        seasonality: {
            type: String,
            required: true
        }
    },
    {
        timestamps: false,
    }
);

const Rewards = mongoose.model(
    'rewards',
    rewardsSchema,
  );

module.exports = Rewards;