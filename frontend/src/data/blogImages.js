import friedChicken from '../assets/blog/blog-fried-chicken.jpg';
import combo from '../assets/blog/blog-combo.jpg';
import burger from '../assets/blog/blog-burger.jpg';
import fries from '../assets/blog/blog-fries.jpg';
import drink from '../assets/blog/blog-drink.jpg';
import newDish from '../assets/blog/blog-new-dish.jpg';

const blogImages = { friedChicken, combo, burger, fries, drink, newDish };

export const getBlogImage = (imageKey) => blogImages[imageKey] ?? friedChicken;
