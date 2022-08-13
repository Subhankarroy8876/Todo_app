import streamlit as st
import pandas as pd 
from db_fxns import create_table,add_data,view_all_data,view_all_task_names,get_task,get_task_by_status,edit_task_data,delete_data
import streamlit.components.v1 as stc


import plotly.express as px 


HTML_BANNER = """
    <h1 style="color:white;text-align:center;">Task Report </h1>
	<p>
	<i class="fa-solid fa
    </div>
    """


def main():
	st.set_page_config(layout="wide")


	menu = ["Create","Read","Update","Delete"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()

	if choice == "Create":
		st.subheader("Add Item")
		
		col1,col2,col3,col4  = st.columns(4)
		with col1:
			task = st.text_input("Task To Do")

		with col2:
			task_status = st.selectbox("Status",["ToDo","Doing","Done","On-Hold"])
			
		with col3:
			task_due_date = st.date_input("Due Date")
		
		with col4:
			priority  = st.selectbox("Prority",["High","Medium","Low"])
			

		if st.button("Add Task"):
			if task=="":
				st.write('Please enter task name!!')
			else:
				add_data(task,task_status,task_due_date,priority)
				st.balloons()

		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date","Priority"])
		left, middle, right = st.columns((2,3,2))
		with middle:
			st.subheader("Your tasks")
			st.dataframe(clean_df)




	elif choice == "Report":
		stc.html(HTML_BANNER)
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date","Priority"])
		col1,col2,col3,col4,col5,col6 = st.columns(6)
		with col2:
			
				task_df = clean_df['Status'].value_counts().to_frame()
				task_df = task_df.reset_index()
				st.dataframe(task_df)
				
		with col5:
			
				task_df_2 = clean_df['Priority'].value_counts().to_frame()
				task_df_2 = task_df_2.reset_index()
				st.dataframe(task_df_2)

		col_1,col_2=st.columns(2)
		with col_1:
			p1 = px.pie(task_df,names='index',values='Status')
			st.plotly_chart(p1,use_container_width=True)
		with col_2:
			p2 = px.pie(task_df_2,names='index',values='Priority')
			st.plotly_chart(p2,use_container_width=True)



	elif choice == "Update":
		st.subheader("Edit Items")
		with st.expander("Current Data"):
			result = view_all_data()
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date","Priority"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Task",list_of_tasks)
		task_result = get_task(selected_task)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			col1,col2 = st.columns(2)
			
			with col1:
				new_task = st.text_area("Task To Do",task)

			with col2:
				new_task_status = st.selectbox(task_status,["ToDo","Doing","Done"])
				new_task_due_date = st.date_input(task_due_date)

			if st.button("Update Task"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Updated :)")

			with st.expander("View Updated Data"):
				result = view_all_data()
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date","Priority"])
				st.dataframe(clean_df)


	elif choice == "Delete":
		st.subheader("Delete")
		with st.expander("View Data"):
			result = view_all_data()
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date","Priority"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Select Task",unique_list)
		if st.button("Delete"):
			delete_data(delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))

		with st.expander("Updated Data"):
			result = view_all_data()
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date","Priority"])
			st.dataframe(clean_df)
			
	else:
		print("Nothing selected")


if __name__ == '__main__':
	main()

