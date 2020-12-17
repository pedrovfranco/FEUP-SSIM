const mongoose = require('mongoose');

const employeesSchema = new mongoose.Schema(
    {
        id: {
            type: Number,
            required: true
        },
        storeId: {
            type: Number,
            required: true
        },
        effortPoints: {
            type: Number,
            required: true
        },
        rewardPoints: {
            type: Number,
            required: true
        }
    },
    {
        timestamps: false,
    }
);

const Employees = mongoose.model(
    'employees',
    employeesSchema,
  );

module.exports = Employees;