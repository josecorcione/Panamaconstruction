import streamlit as st
import datetime

def setup_session_state():
    if 'role' not in st.session_state:
        st.session_state['role'] = None
    if 'projects' not in st.session_state:
        st.session_state['projects'] = []
    if 'materials' not in st.session_state:
        st.session_state['materials'] = []
    if 'bids' not in st.session_state:
        st.session_state['bids'] = []
    if 'orders' not in st.session_state:
        st.session_state['orders'] = []
    if 'categories' not in st.session_state:
        st.session_state['categories'] = {
            "Concrete & Cement": ["Ready Mix", "Cement Bags", "Aggregates"],
            "Steel & Metals": ["Rebar", "Structural Steel", "Sheet Metal"],
            "Plumbing": ["PVC Pipes", "Copper Pipes", "Fittings", "Fixtures"],
            "Electrical": ["Wiring", "Conduit", "Panels", "Fixtures"],
            "Lumber & Wood": ["Plywood", "Dimensional Lumber", "Finishing Wood"],
            "Finishes": ["Paint", "Tiles", "Flooring", "Drywall"],
            "Tools & Equipment": ["Power Tools", "Hand Tools", "Safety Equipment"]
        }
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = f"user_{datetime.datetime.now().timestamp()}"

def add_sample_data():
    if not st.session_state.projects:
        st.session_state.projects.extend([
            {
                "title": "Luxury Apartments in Costa del Este",
                "location": "Costa del Este, Panama",
                "type": "High-rise Residential",
                "budget": 15000000,
                "description": "20-story luxury apartment building with ocean view",
                "status": "Open",
                "date_posted": datetime.datetime.now().strftime("%Y-%m-%d"),
                "files": [],  # Files will be stored in session state
                "bids": []
            },
            {
                "title": "Commercial Complex in Obarrio",
                "location": "Obarrio, Panama",
                "type": "Commercial Office",
                "budget": 8000000,
                "description": "Modern office complex with retail space",
                "status": "Open",
                "date_posted": datetime.datetime.now().strftime("%Y-%m-%d"),
                "files": [],
                "bids": []
            }
        ])
    if not st.session_state.materials:
        st.session_state.materials.extend([
            {
                "name": "Portland Cement (94lb bag)",
                "category": "Concrete & Cement",
                "subcategory": "Cement Bags",
                "supplier": "Argos",
                "price": 8.50,
                "availability": "In Stock",
                "location": "Panama City",
                "contact": "6678-9900",
                "minimum_order": 10
            },
            {
                "name": "PVC Pipe 4\" (6m length)",
                "category": "Plumbing",
                "subcategory": "PVC Pipes",
                "supplier": "Tuberias SA",
                "price": 12.75,
                "availability": "In Stock",
                "location": "Panama City",
                "contact": "6789-0123",
                "minimum_order": 5
            }
        ])

def main():
    setup_session_state()
    add_sample_data()

    st.title("Panama Construction Platform")

    if st.session_state.role == "Developer":
        show_developer_interface()
    elif st.session_state.role == "Contractor":
        show_contractor_interface()
    elif st.session_state.role == "Supplier":
        show_supplier_interface()
    else:
        show_role_selection()

def show_role_selection():
    st.header("Welcome to Panama Construction Platform")
    st.subheader("Select your role to continue:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Developer"):
            st.session_state.role = "Developer"
    with col2:
        if st.button("Contractor"):
            st.session_state.role = "Contractor"
    with col3:
        if st.button("Supplier"):
            st.session_state.role = "Supplier"

    # Instructions for each role
    with col1:
        st.write("Post projects and review bids")
    with col2:
        st.write("Find projects and order materials")
    with col3:
        st.write("Manage materials and track orders")

def reset_role():
    st.session_state.role = None

def show_developer_interface():
    st.sidebar.button("← Back to Role Selection", on_click=reset_role)
    st.header("Developer Dashboard")
    tab1, tab2 = st.tabs(["Post New Project", "My Projects"])
    with tab1:
        create_post_project_tab()
    with tab2:
        create_my_projects_tab()

def create_post_project_tab():
    st.subheader("Post New Project")
    with st.form("post_project_form"):
        title = st.text_input("Project Title:*")
        location = st.text_input("Location:*")
        project_type = st.selectbox("Project Type:*", [
                "High-rise Residential",
                "Commercial Office",
                "Commercial Retail",
                "Industrial",
                "Healthcare",
                "Infrastructure",
                "Renovation"
            ])
        budget = st.text_input("Budget (USD):*")
        description = st.text_area("Description:*")
        uploaded_files = st.file_uploader("Upload Project Files", accept_multiple_files=True)
        submitted = st.form_submit_button("Submit Project")
        if submitted:
            if not all([title, location, project_type, budget, description]):
                st.error("Please fill in all required fields")
            else:
                try:
                    budget = float(budget)
                    project_files = []
                    for uploaded_file in uploaded_files:
                        file_data = uploaded_file.read()
                        file_info = {
                            'name': uploaded_file.name,
                            'data': file_data,
                            'type': uploaded_file.type
                        }
                        project_files.append(file_info)
                    new_project = {
                        "title": title,
                        "location": location,
                        "type": project_type,
                        "budget": budget,
                        "description": description,
                        "status": "Open",
                        "date_posted": datetime.datetime.now().strftime("%Y-%m-%d"),
                        "files": project_files,
                        "bids": []
                    }
                    st.session_state.projects.append(new_project)
                    st.success("Project posted successfully!")
                except ValueError:
                    st.error("Please enter a valid budget amount")

def create_my_projects_tab():
    st.subheader("My Projects")
    projects = st.session_state.projects
    if projects:
        for project in projects:
            with st.expander(project['title']):
                st.write(f"**Location:** {project['location']}")
                st.write(f"**Type:** {project['type']}")
                st.write(f"**Budget:** ${project['budget']:,.2f}")
                st.write(f"**Status:** {project['status']}")
                st.write(f"**Posted on:** {project['date_posted']}")
                st.write(f"**Description:** {project['description']}")
                if project['files']:
                    st.write("**Files:**")
                    for file_info in project['files']:
                        st.download_button(label=file_info['name'], data=file_info['data'],
                                           file_name=file_info['name'])
                else:
                    st.write("No files uploaded")
                if project['bids']:
                    st.write(f"**Bids Received:** {len(project['bids'])}")
                    for bid in project['bids']:
                        st.write(f"- {bid['contractor']}: ${bid['amount']:,.2f}, Timeline: {bid['timeline']} days")
                else:
                    st.write("No bids received yet")
    else:
        st.write("You have no projects")

def show_contractor_interface():
    st.sidebar.button("← Back to Role Selection", on_click=reset_role)
    st.header("Contractor Dashboard")
    tab1, tab2, tab3, tab4 = st.tabs(["Available Projects", "My Bids", "Materials Search", "My Orders"])
    with tab1:
        create_available_projects_tab()
    with tab2:
        create_my_bids_tab()
    with tab3:
        create_materials_search_tab()
    with tab4:
        create_orders_tab()

def create_available_projects_tab():
    st.subheader("Available Projects")
    search_text = st.text_input("Search")
    selected_location = st.selectbox("Location", ['All', 'Panama City', 'Costa del Este', 'Obarrio', 
                        'San Francisco', 'Punta Pacifica', 'Clayton', 'Other'])
    selected_type = st.selectbox("Project Type", [
        "All",
        "High-rise Residential",
        "Commercial Office",
        "Commercial Retail",
        "Industrial",
        "Healthcare",
        "Infrastructure",
        "Renovation"
    ])
    min_budget = st.text_input("Min Budget (USD)")
    max_budget = st.text_input("Max Budget (USD)")
    projects = st.session_state.projects
    filtered_projects = []
    try:
        min_budget = float(min_budget) if min_budget else 0
        max_budget = float(max_budget) if max_budget else float('inf')
    except ValueError:
        st.error("Please enter valid budget amounts")
        return
    for project in projects:
        if search_text.lower() not in project['title'].lower():
            continue
        if selected_location != 'All' and project['location'] != selected_location:
            continue
        if selected_type != 'All' and project['type'] != selected_type:
            continue
        if not (min_budget <= project['budget'] <= max_budget):
            continue
        filtered_projects.append(project)
    if filtered_projects:
        for project in filtered_projects:
            with st.expander(project['title']):
                st.write(f"**Location:** {project['location']}")
                st.write(f"**Type:** {project['type']}")
                st.write(f"**Budget:** ${project['budget']:,.2f}")
                st.write(f"**Status:** {project['status']}")
                st.write(f"**Posted on:** {project['date_posted']}")
                st.write(f"**Description:** {project['description']}")
                if project['files']:
                    st.write("**Files:**")
                    for file_info in project['files']:
                        st.download_button(label=file_info['name'], data=file_info['data'],
                                           file_name=file_info['name'])
                else:
                    st.write("No files uploaded")
                st.write("### Submit Bid")
                with st.form(f"bid_form_{project['title']}"):
                    amount = st.text_input("Bid Amount ($):*")
                    timeline = st.text_input("Timeline (days):*")
                    company = st.text_input("Company Name:*")
                    contact = st.text_input("Contact Person:*")
                    phone = st.text_input("Phone:*")
                    email = st.text_input("Email:*")
                    license = st.text_input("License Number:*")
                    approach = st.text_area("Project Approach:*")
                    experience = st.text_area("Similar Projects Experience:*")
                    bid_files = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True)
                    submitted = st.form_submit_button("Submit Bid")
                    if submitted:
                        if not all([amount, timeline, company, contact, phone, email, license, approach, experience]):
                            st.error("Please fill in all required fields")
                        else:
                            try:
                                amount = float(amount)
                                timeline = int(timeline)
                                if amount > project['budget'] * 1.2:
                                    st.warning("Your bid is significantly over the project budget.")
                                bid_files_list = []
                                for uploaded_file in bid_files:
                                    file_data = uploaded_file.read()
                                    file_info = {
                                        'name': uploaded_file.name,
                                        'data': file_data,
                                        'type': uploaded_file.type
                                    }
                                    bid_files_list.append(file_info)
                                new_bid = {
                                    "amount": amount,
                                    "timeline": timeline,
                                    "contractor": company,
                                    "contact": contact,
                                    "phone": phone,
                                    "email": email,
                                    "license": license,
                                    "approach": approach,
                                    "experience": experience,
                                    "files": bid_files_list,
                                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                                    "status": "Submitted",
                                    "status_history": [{
                                        "status": "Submitted",
                                        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                                        "notes": "Bid submitted successfully"
                                    }],
                                    "user_id": st.session_state.user_id  # To associate bid with user
                                }
                                project['bids'].append(new_bid)
                                st.success("Bid submitted successfully!")
                            except ValueError:
                                st.error("Please enter valid numbers for amount and timeline")
    else:
        st.write("No projects found matching the criteria")

def create_my_bids_tab():
    st.subheader("My Bids")
    status_filter = st.selectbox("Status", ['All', 'Submitted', 'Under Review', 'Awarded', 'Not Selected', 'Pending'])
    bids = []
    for project in st.session_state.projects:
        for bid in project.get('bids', []):
            if bid.get('user_id') == st.session_state.user_id:
                bids.append({
                    'project_title': project['title'],
                    'location': project['location'],
                    'amount': bid['amount'],
                    'timeline': bid['timeline'],
                    'date': bid['date'],
                    'status': bid['status'],
                    'notes': bid.get('notes', ''),
                    'approach': bid.get('approach', ''),
                    'experience': bid.get('experience', ''),
                    'files': bid.get('files', [])
                })
    filtered_bids = [bid for bid in bids if status_filter == 'All' or bid['status'] == status_filter]
    if filtered_bids:
        for bid in filtered_bids:
            with st.expander(f"Bid for {bid['project_title']}"):
                st.write(f"**Project:** {bid['project_title']}")
                st.write(f"**Location:** {bid['location']}")
                st.write(f"**Amount:** ${bid['amount']:,.2f}")
                st.write(f"**Timeline:** {bid['timeline']} days")
                st.write(f"**Date:** {bid['date']}")
                st.write(f"**Status:** {bid['status']}")
                st.write(f"**Notes:** {bid['notes']}")
                st.write(f"**Project Approach:** {bid['approach']}")
                st.write(f"**Experience:** {bid['experience']}")
                if bid['files']:
                    st.write("**Supporting Documents:**")
                    for file_info in bid['files']:
                        st.download_button(label=file_info['name'], data=file_info['data'],
                                           file_name=file_info['name'])
    else:
        st.write("No bids found")

def create_materials_search_tab():
    st.subheader("Materials Search")
    search_text = st.text_input("Search")
    category = st.selectbox("Category", ['All Categories'] + list(st.session_state.categories.keys()))
    subcategory = 'All'
    if category != 'All Categories':
        subcategories = st.session_state.categories.get(category, [])
        subcategory = st.selectbox("Subcategory", ['All'] + subcategories)
    location = st.selectbox("Location", ['All', 'Panama City', 'Costa del Este', 'Obarrio', 
                                      'San Francisco', 'Punta Pacifica', 'Clayton'])
    availability = st.selectbox("Availability", ['All', 'In Stock', 'Limited Stock', 'Out of Stock'])
    min_price = st.text_input("Min Price (USD)")
    max_price = st.text_input("Max Price (USD)")
    materials = st.session_state.materials
    filtered_materials = []
    try:
        min_price = float(min_price) if min_price else 0
        max_price = float(max_price) if max_price else float('inf')
    except ValueError:
        st.error("Please enter valid price amounts")
        return
    for material in materials:
        if search_text.lower() not in material['name'].lower():
            continue
        if category != 'All Categories' and material['category'] != category:
            continue
        if subcategory != 'All' and material['subcategory'] != subcategory:
            continue
        if location != 'All' and material['location'] != location:
            continue
        if availability != 'All' and material['availability'] != availability:
            continue
        if not (min_price <= material['price'] <= max_price):
            continue
        filtered_materials.append(material)
    if filtered_materials:
        for material in filtered_materials:
            with st.expander(material['name']):
                st.write(f"**Category:** {material['category']} - {material['subcategory']}")
                st.write(f"**Price:** ${material['price']:.2f}")
                st.write(f"**Supplier:** {material['supplier']}")
                st.write(f"**Location:** {material['location']}")
                st.write(f"**Availability:** {material['availability']}")
                st.write(f"**Minimum Order:** {material['minimum_order']}")
                st.write("### Place Order")
                with st.form(f"order_form_{material['name']}"):
                    quantity = st.text_input("Quantity:*", value=str(material['minimum_order']))
                    delivery_date = st.date_input("Delivery Date:*", min_value=datetime.datetime.now().date())
                    delivery_address = st.text_area("Delivery Address:*")
                    project_name = st.text_input("Project Name:*")
                    instructions = st.text_area("Special Instructions:")
                    contact_person = st.text_input("Contact Person:*")
                    contact_phone = st.text_input("Contact Phone:*")
                    submitted = st.form_submit_button("Place Order")
                    if submitted:
                        if not all([quantity, delivery_date, delivery_address, project_name, contact_person, contact_phone]):
                            st.error("Please fill in all required fields")
                        else:
                            try:
                                quantity = int(quantity)
                                if quantity < material['minimum_order']:
                                    st.error(f"Minimum order quantity is {material['minimum_order']}")
                                    return
                                new_order = {
                                    "order_id": f"ORD-{len(st.session_state.orders) + 1:04d}",
                                    "material": material['name'],
                                    "supplier": material['supplier'],
                                    "quantity": quantity,
                                    "price_per_unit": material['price'],
                                    "total_price": quantity * material['price'],
                                    "delivery_date": delivery_date.strftime("%Y-%m-%d"),
                                    "delivery_address": delivery_address,
                                    "project_name": project_name,
                                    "instructions": instructions,
                                    "status": "Pending",
                                    "order_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                                    "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "contact_person": contact_person,
                                    "contact_phone": contact_phone,
                                    "user_id": st.session_state.user_id  # Associate order with user
                                }
                                st.session_state.orders.append(new_order)
                                st.success(f"Order placed successfully!\nOrder ID: {new_order['order_id']}")
                            except ValueError:
                                st.error("Please enter a valid quantity")
    else:
        st.write("No materials found matching the criteria")

def create_orders_tab():
    st.subheader("My Orders")
    status_filter = st.selectbox("Status", ['All', 'Pending', 'Confirmed', 'In Transit', 'Delivered', 'Cancelled'])
    orders = [order for order in st.session_state.orders if order.get('user_id') == st.session_state.user_id]
    filtered_orders = [order for order in orders if status_filter == 'All' or order['status'] == status_filter]
    if filtered_orders:
        for order in filtered_orders:
            with st.expander(f"Order {order['order_id']} - {order['material']}"):
                st.write(f"**Order ID:** {order['order_id']}")
                st.write(f"**Material:** {order['material']}")
                st.write(f"**Quantity:** {order['quantity']}")
                st.write(f"**Total Price:** ${order['total_price']:.2f}")
                st.write(f"**Supplier:** {order['supplier']}")
                st.write(f"**Order Date:** {order['order_date']}")
                st.write(f"**Delivery Date:** {order['delivery_date']}")
                st.write(f"**Delivery Address:** {order['delivery_address']}")
                st.write(f"**Project Name:** {order['project_name']}")
                st.write(f"**Status:** {order['status']}")
                st.write(f"**Last Updated:** {order['last_updated']}")
    else:
        st.write("No orders found")

def show_supplier_interface():
    st.sidebar.button("← Back to Role Selection", on_click=reset_role)
    st.header("Supplier Dashboard")
    tab1, tab2, tab3 = st.tabs(["Add New Material", "My Materials", "View Orders"])
    with tab1:
        create_add_materials_tab()
    with tab2:
        create_my_materials_tab()
    with tab3:
        create_supplier_orders_tab()

def create_add_materials_tab():
    st.subheader("Add New Material")
    with st.form("add_material_form"):
        name = st.text_input("Material Name:*")
        category = st.selectbox("Category:*", list(st.session_state.categories.keys()))
        subcategories = st.session_state.categories.get(category, [])
        subcategory = st.selectbox("Subcategory:*", subcategories)
        price = st.text_input("Price (USD):*")
        min_order = st.text_input("Minimum Order Quantity:*")
        location = st.text_input("Location:*")
        contact = st.text_input("Contact Number:*")
        availability = st.selectbox("Availability:*", [
                "In Stock",
                "Limited Stock",
                "Out of Stock",
                "Available on Order"
            ])
        submitted = st.form_submit_button("Add Material")
        if submitted:
            if not all([name, category, subcategory, price, min_order, location, contact, availability]):
                st.error("Please fill in all required fields")
            else:
                try:
                    new_material = {
                        "name": name,
                        "category": category,
                        "subcategory": subcategory,
                        "price": float(price),
                        "minimum_order": int(min_order),
                        "location": location,
                        "contact": contact,
                        "availability": availability,
                        "supplier": "Your Company",
                        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.materials.append(new_material)
                    st.success("Material added successfully!")
                except ValueError:
                    st.error("Please enter valid numbers for price and minimum order")

def create_my_materials_tab():
    st.subheader("My Materials")
    category_filter = st.selectbox("Category", ['All'] + list(st.session_state.categories.keys()))
    availability_filter = st.selectbox("Availability", ['All', 'In Stock', 'Limited Stock', 'Out of Stock'])
    materials = [material for material in st.session_state.materials if material['supplier'] == "Your Company"]
    filtered_materials = [material for material in materials if
                          (category_filter == 'All' or material['category'] == category_filter) and
                          (availability_filter == 'All' or material['availability'] == availability_filter)]
    if filtered_materials:
        for material in filtered_materials:
            with st.expander(material['name']):
                st.write(f"**Category:** {material['category']} - {material['subcategory']}")
                st.write(f"**Price:** ${material['price']:.2f}")
                st.write(f"**Minimum Order:** {material['minimum_order']}")
                st.write(f"**Availability:** {material['availability']}")
                st.write(f"**Location:** {material['location']}")
                st.write(f"**Contact Number:** {material['contact']}")
                st.write(f"**Last Updated:** {material['last_updated']}")
                st.write("### Edit Material")
                with st.form(f"edit_material_form_{material['name']}"):
                    price = st.text_input("Price (USD):*", value=str(material['price']))
                    min_order = st.text_input("Minimum Order Quantity:*", value=str(material['minimum_order']))
                    availability = st.selectbox("Availability:*", [
                            "In Stock",
                            "Limited Stock",
                            "Out of Stock",
                            "Available on Order"
                        ], index=["In Stock", "Limited Stock", "Out of Stock", "Available on Order"].index(material['availability']))
                    submitted = st.form_submit_button("Save Changes")
                    if submitted:
                        try:
                            material['price'] = float(price)
                            material['minimum_order'] = int(min_order)
                            material['availability'] = availability
                            material['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                            st.success("Material updated successfully!")
                        except ValueError:
                            st.error("Please enter valid numbers for price and minimum order")
    else:
        st.write("No materials found")

def create_supplier_orders_tab():
    st.subheader("View Orders")
    status_filter = st.selectbox("Status", ['All', 'Pending', 'Confirmed', 'In Transit', 'Delivered', 'Cancelled'])
    orders = [order for order in st.session_state.orders if order['supplier'] == "Your Company"]
    filtered_orders = [order for order in orders if status_filter == 'All' or order['status'] == status_filter]
    if filtered_orders:
        for order in filtered_orders:
            with st.expander(f"Order {order['order_id']} - {order['material']}"):
                st.write(f"**Order ID:** {order['order_id']}")
                st.write(f"**Material:** {order['material']}")
                st.write(f"**Quantity:** {order['quantity']}")
                st.write(f"**Total Price:** ${order['total_price']:.2f}")
                st.write(f"**Customer:** {order['contact_person']}")
                st.write(f"**Phone:** {order['contact_phone']}")
                st.write(f"**Order Date:** {order['order_date']}")
                st.write(f"**Delivery Date:** {order['delivery_date']}")
                st.write(f"**Delivery Address:** {order['delivery_address']}")
                st.write(f"**Status:** {order['status']}")
                st.write(f"**Last Updated:** {order['last_updated']}")
                st.write("### Update Status")
                with st.form(f"update_status_form_{order['order_id']}"):
                    new_status = st.selectbox("Update Status", ['Pending', 'Confirmed', 'In Transit', 'Delivered', 'Cancelled'], index=['Pending', 'Confirmed', 'In Transit', 'Delivered', 'Cancelled'].index(order['status']))
                    submitted = st.form_submit_button("Update Status")
                    if submitted:
                        order['status'] = new_status
                        order['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.success("Order status updated successfully!")
    else:
        st.write("No orders found")

if __name__ == "__main__":
    main()
