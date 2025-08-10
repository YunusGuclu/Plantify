import { reactive, computed } from 'vue';

// Simple cart store using localStorage for persistence
const state = reactive({
  items: JSON.parse(localStorage.getItem('cart') || '[]')
});

function save() {
  localStorage.setItem('cart', JSON.stringify(state.items));
}

export function useCart() {
  return {
    cart: state,
    addToCart(item) {
      state.items.push(item);
      save();
    },
    removeFromCart(index) {
      state.items.splice(index, 1);
      save();
    },
    clearCart() {
      state.items = [];
      save();
    },
    cartCount: computed(() => state.items.length),
    totalPrice: computed(() => state.items.reduce((sum, i) => sum + i.price, 0))
  };
}