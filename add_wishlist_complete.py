"""
Complete script to add all wishlist functionality to base.html
"""

def add_wishlist_to_base():
    file_path = r'templates\base.html'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    
    # 1. Add wishlist icon before cart icon (desktop)
    wishlist_icon = '''                <!-- Wishlist Icon -->
                <a href="{% url 'products:wishlist' %}"
                    class="relative inline-flex items-center justify-center w-10 h-10 rounded-full hover:bg-zinc-100 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="text-zinc-900">
                        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
                    </svg>
                    <span
                        class="wishlist-badge absolute -top-1 -right-1 bg-red-500 text-white text-[10px] font-bold h-5 w-5 flex items-center justify-center rounded-full border-2 border-white hidden">
                        0
                    </span>
                </a>

'''
    
    # Find and insert before cart icon
    for i, line in enumerate(lines):
        if '                <a href="{% url \'orders:view_cart\' %}"' in line and 'Wishlist Icon' not in ''.join(lines[max(0,i-5):i]):
            lines.insert(i, wishlist_icon)
            modified = True
            print("✓ Added wishlist icon to desktop navbar")
            break
    
    # 2. Add wishlist link to mobile  menu
    for i, line in enumerate(lines):
        if '                    <a href="{% url \'orders:order_history\' %}"' in line and 'class="block py-2 text-lg font-medium text-zinc-900">Orders</a>' in lines[i+1]:
            # Check if wishlist not already added
            if 'wishlist' not in lines[i+2].lower():
                wishlist_mobile = '                    <a href="{% url \'products:wishlist\' %}"\r\n                        class="block py-2 text-lg font-medium text-zinc-900">Wishlist</a>\r\n'
                lines.insert(i+2, wishlist_mobile)
                modified = True
                print("✓ Added wishlist link to mobile menu")
            break
    
    # Write back
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("\n✅ Successfully updated base.html with wishlist icon!")
    else:
        print("ℹ Wishlist icon already exists or couldn't find insertion point")

if __name__ == '__main__':
    add_wishlist_to_base()
