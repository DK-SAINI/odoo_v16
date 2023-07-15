# Sale Order Test Cases

This repository contains test cases for the sale order module in Odoo. The test cases are implemented using Python and Odoo's testing framework.

## Getting Started

To run the test cases, you need to have Odoo installed and configured. Please refer to the official Odoo documentation for installation instructions.

## Running the Tests

1. Clone this repository to your local machine.
2. Navigate to the repository's directory.
3. Activate your Odoo development environment.
4. Run the following command to execute the test cases:

```bash
odoo-bin -c <path-to-odoo-configuration-file> -d <database-name> -i <module-to-test> --test-enable --stop-after-init
```
Replace <path-to-odoo-configuration-file> with the path to your Odoo configuration file, <database-name> with the name of the database you want to use for testing, and <module-to-test> with the name of the module containing the sale order test cases.


## Test Cases

The following test cases are included in this repository:

   - test_create_sale_order: Tests the creation of a sale order and verifies the partner, date, and initial state.
   - test_confirm_sale_order: Tests the confirmation of a sale order and verifies the state change to 'sale'.
   - test_cancel_sale_order: Tests the cancellation of a sale order and verifies the state change to 'cancel'.

Feel free to customize and add more test cases based on your specific requirements.

## Contributing

- If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

In this README.md file, we provide an overview of the repository and the steps to run the test cases. We explain how to clone the repository, activate the Odoo development environment, and execute the test cases using the Odoo command line. We list the available test cases and briefly describe each one. We also mention that contributors are welcome to open issues or submit pull requests, and we specify the license under which the project is released.

Make sure to update the instructions and details according to your specific project setup and requirements.
