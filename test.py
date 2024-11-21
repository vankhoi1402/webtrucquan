import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#data
df=pd.read_csv('baucu.csv')
data=pd.read_csv('baucu.csv')

st.write(df.head(10))
#làm dữ liệu 
votes_per_state=df.groupby('state_name')[['votes_gop', 'votes_dem']].sum().sort_values('votes_dem')
# Sắp xếp dữ liệu
state_votes = data.groupby("state_name").agg(
    avg_gop=("per_gop", "mean"), avg_dem=("per_dem", "mean")
).reset_index()



#sidebar
st.sidebar.title("Tùy chọn hiển thị biểu đồ")
chart_type = st.sidebar.selectbox("Chọn bảng dữ liệu trực quan", 
                                  ["Hiển thị tổng số phiếu bầu cho GOP theo từng bang", 
                                   "Hiển thị tỷ lệ phần trăm phiếu của GOP và Đảng Dân chủ",  
                                   "Hiển thị xu hướng phần trăm phiếu của GOP trên các quận trong một bang được chọn.",
                                   "Tỷ Lệ Bỏ Phiếu Của Đảng Cộng Hòa vs. Đảng Dân Chủ Theo Bang",
                                   "Phân Phối Tỷ Lệ Bỏ Phiếu Theo Cấp Hạt",
                                   "Các Hạt Có Chênh Lệch Bỏ Phiếu Cao Nhất",
                                   "Biểu đồ kết quả bầu cử"
                                   ])
#tieu de
st.title("Bầu cử tổng thống Mĩ 2020")




#  - Hiển thị tổng số phiếu bầu cho GOP theo từng bang
if chart_type == "Hiển thị tổng số phiếu bầu cho GOP theo từng bang":
    choses1_type = st.sidebar.selectbox('Chọn đảng', [
        'Đảng Cộng Hòa',
        'Đảng Dân Chủ'
    ])
    if choses1_type == 'Đảng Cộng Hòa':
        st.subheader("Hiển thị tổng số phiếu bầu cho GOP theo từng bang")
        fig1, ax1 = plt.subplots(figsize=(12, 8))
        votes_per_state['votes_gop'].plot(kind='barh', color='skyblue', ax=ax1)
        ax1.set_title('Hiển thị tổng số phiếu bầu cho GOP theo từng bang')
        ax1.set_xlabel('Total GOP Votes')
        ax1.set_ylabel('State')
        st.pyplot(fig1)
    else:
        st.subheader("Hiển thị tổnng số phiếu bầu cho Đảng Dân Chủ theo từng bang")
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        votes_per_state['votes_dem'].plot(kind='barh', color='skyblue', ax=ax2)
        ax2.set_title('Hiển thị tổng số phiếu bầu cho Đảng Dân Chủ theo từng bang')
        ax2.set_xlabel('Total Dem Votes')
        ax2.set_ylabel('State')
        st.pyplot(fig2)
# bieu dồ tròn Hiển thị tỷ lệ phần trăm phiếu của GOP và Đảng Dân chủ
elif chart_type == "Hiển thị tỷ lệ phần trăm phiếu của GOP và Đảng Dân chủ":
    st.subheader("Hiển thị tỷ lệ phần trăm phiếu của GOP và Đảng Dân chủ trong một bang cụ thể.")
    selected_state = st.sidebar.selectbox("Chọn bang", votes_per_state.index)
    votes_in_state = votes_per_state.loc[selected_state]
    st.write(votes_in_state)
    fig3, ax3 = plt.subplots()
    ax3.set_title(f'Phần trăm bỏ phiếu tại {selected_state}')
    st.pyplot(fig3)
#  Line Chart - Hiển thị xu hướng phần trăm phiếu của GOP trên các quận trong một bang được chọn.
elif chart_type == "Hiển thị xu hướng phần trăm phiếu của GOP trên các quận trong một bang được chọn.":
    st.subheader("Hiển thị xu hướng phần trăm phiếu của GOP trên các quận trong một bang được chọn.")
    selected_state = st.sidebar.selectbox("Select a state for GOP percentage trend", df['state_name'].unique())
    state_data = df[df['state_name'] == selected_state].sort_values('county_fips')
    fig5, ax5 = plt.subplots(figsize=(12, 8))
    ax5.plot(state_data['county_name'], state_data['per_gop'], marker='o', color='green')
    ax5.set_title(f'GOP Vote Percentage Across Counties in {selected_state}')
    ax5.set_xlabel('County')
    ax5.set_ylabel('GOP Vote Percentage')
    ax5.tick_params(axis='x', rotation=90)
    st.pyplot(fig5)
    #ket qua bau cu
elif chart_type == "Biểu đồ kết quả bầu cử":
    st.subheader("Hiển thị kết quả bầu cử")
    GOP_CHOICES =df['votes_gop'].sum()
    DEM_CHOICES = df['votes_dem'].sum()
    total_votes =[df['votes_gop'].sum(), df['votes_dem'].sum()]
    labels = ['GOP', 'Dem']
    fig7, ax7 = plt.subplots(figsize=(12, 8))
    ax7=plt.bar(labels,total_votes ,color='skyblue')
    for bar in ax7:
        plt.text(    
            bar.get_x() + bar.get_width() / 2,  # Tọa độ x
            bar.get_height() + 50,             # Tọa độ y
            f'{int(bar.get_height())}',        # Giá trị
            ha='center', va='bottom', fontsize=10
        )
    st.pyplot(fig7)
    #thanh lam
elif chart_type == "Tỷ Lệ Bỏ Phiếu Của Đảng Cộng Hòa vs. Đảng Dân Chủ Theo Bang":
    st.header("Tỷ Lệ Bỏ Phiếu Của Đảng Cộng Hòa vs. Đảng Dân Chủ Theo Bang")
    # Lựa chọn sắp xếp từ sidebar
    sort_option = st.sidebar.selectbox(
        "Sắp xếp các bang theo:",
        options=["Tỷ lệ GOP giảm dần", "Tỷ lệ DEM giảm dần"]
    )
    if sort_option == "Tỷ lệ GOP giảm dần":
     state_votes = state_votes.sort_values(by="avg_gop", ascending=False)
    else:
     state_votes = state_votes.sort_values(by="avg_dem", ascending=False)
    # Hiển thị biểu đồ
    fig1, ax1 = plt.subplots(figsize=(12, 8))
    sns.barplot(
        x="avg_gop", y="state_name", data=state_votes, color="red", label="Đảng Cộng Hòa", ax=ax1
    )
    sns.barplot(
        x="avg_dem", y="state_name", data=state_votes, color="blue", label="Đảng Dân Chủ", ax=ax1
    )
    ax1.set_xlabel("Tỷ Lệ Phiếu Bầu Trung Bình")
    ax1.set_ylabel("Bang")
    ax1.legend()
    st.pyplot(fig1)
elif chart_type == "Phân Phối Tỷ Lệ Bỏ Phiếu Theo Cấp Hạt":
    # 2. Phân Phối Tỷ Lệ Bỏ Phiếu Theo Cấp Hạt
    st.header("Phân Phối Tỷ Lệ Bỏ Phiếu Theo Cấp Hạt")

    # Điều chỉnh số lượng bins cho biểu đồ phân phối
    bins = st.sidebar.slider("Số lượng bins", min_value=10, max_value=50, value=30, step=5)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.histplot(data["per_point_diff"].abs(), bins=bins, kde=True, color="purple", ax=ax2)
    ax2.set_title("Phân Phối Chênh Lệch Tỷ Lệ Phiếu Bầu Đảng Cộng Hòa vs. Đảng Dân Chủ")
    ax2.set_xlabel("Chênh Lệch Tỷ Lệ Phần Trăm (Cộng Hòa - Dân Chủ)")
    st.pyplot(fig2)
elif chart_type == "Các Hạt Có Chênh Lệch Bỏ Phiếu Cao Nhất":
    # 3. Các Hạt Có Chênh Lệch Bỏ Phiếu Cao Nhất
    st.header("Các Hạt Có Chênh Lệch Bỏ Phiếu Cao Nhất")

    # Điều chỉnh số lượng hạt hiển thị
    top_counties_count = st.sidebar.slider("Số lượng hạt hiển thị", min_value=5, max_value=20, value=10, step=1)

    # Lấy các hạt có chênh lệch phiếu bầu lớn nhất
    top_counties = data.nlargest(top_counties_count, "diff")[["county_name", "state_name", "diff"]]

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="diff", y="county_name", data=top_counties, hue="state_name", dodge=False, ax=ax3
    )
    ax3.set_xlabel("Chênh Lệch Phiếu Bầu")
    ax3.set_ylabel("Hạt")
    st.pyplot(fig3)






