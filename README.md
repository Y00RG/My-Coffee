# Coffee Shop Website ☕️

A full-featured coffee shop website built with Django. Users can explore a variety of coffee products, register as members, manage their profiles, add items to their shopping cart, and securely checkout using credit card payments.

## Features

- **User Registration & Login**: Visitors can sign up, log in, and manage their profiles.
- **Coffee Product Listings**: Browse multiple coffee flavors and blends with dynamic product pages.
- **Shopping Cart**: Users can add multiple items to their cart and manage their order before checking out.
- **Profile Management**: Members can update their personal details and view order history.
- **Checkout & Payment**: Secure checkout process integrated with credit card payments.
- **Responsive Design**: Optimized for desktop and mobile viewing.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: PostgreSQL
- **Payment Integration**: (e.g., Stripe or PayPal)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/coffee-shop.git
   cd coffee-shop
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the site**: Go to `http://127.0.0.1:8000/` in your browser.

## Usage

- **Register** a new account or log in to an existing one.
- **Browse** the coffee products and add them to your shopping cart.
- **Checkout** and make payments using your credit card.
- **Manage your profile** and view your order history.

## Contributing

Feel free to contribute to this project by forking the repository and submitting a pull request. You can also open an issue to report bugs or suggest new features.

