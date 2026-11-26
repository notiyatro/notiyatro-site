// Siparişler Netlify Blobs'ta "orders" deposunda tutulur (ek servis gerekmez).
import { getStore } from '@netlify/blobs';
export const orders = () => getStore({ name: 'orders', consistency: 'strong' });
