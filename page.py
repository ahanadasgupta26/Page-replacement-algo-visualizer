import streamlit as st

def fifo_page_replacement(ref_string,num_frames):
    frames=[]
    page_faults=0
    history=[]  

    for page in ref_string:
        if page not in frames:
            page_faults+=1
            if len(frames)<num_frames:
                frames.append(page)
            else:
                frames.pop(0)  
                frames.append(page)
        
        history.append(frames.copy())  

    return page_faults,history

def lru_page_replacement(ref_string,num_frames):
    frames=[]
    page_faults=0
    history=[]
    recent_usage=[]

    for page in ref_string:
        if page not in frames:
            page_faults+=1
            if len(frames)<num_frames:
                frames.append(page)
            else:
                lru_page=recent_usage.pop(0)
                frames.remove(lru_page)
                frames.append(page)
        else:
            recent_usage.remove(page)
        
        recent_usage.append(page)
        history.append(frames.copy())

    return page_faults,history

def mru_page_replacement(ref_string,num_frames):
    frames=[]
    page_faults=0
    history=[]
    recent_usage=[]

    for page in ref_string:
        if page not in frames:
            page_faults+=1
            if len(frames)<num_frames:
                frames.append(page)
            else:
                mru_page=recent_usage.pop()
                frames.remove(mru_page)
                frames.append(page)
        else:
            recent_usage.remove(page)
        
        recent_usage.append(page)
        history.append(frames.copy())

    return page_faults,history

def optimal_page_replacement(ref_string,num_frames):
    frames=[]
    page_faults=0
    history=[]

    for i, page in enumerate(ref_string):
        if page not in frames:
            page_faults+=1
            if len(frames)<num_frames:
                frames.append(page)
            else:
                future_uses=ref_string[i+1:]
                indices=[future_uses.index(f) if f in future_uses else float('inf') for f in frames]
                frames.pop(indices.index(max(indices)))
                frames.append(page)
        
        history.append(frames.copy())

    return page_faults,history

st.title("Page Replacement Algorithms")

algorithm = st.selectbox("Select Algorithm",["FIFO", "LRU", "MRU", "Optimal"])

ref_input = st.text_input("Enter Reference String (comma-separated)","7,0,1,2,0,3,4,2,3,0,3,2")
reference_string = list(map(int,ref_input.split(',')))

num_frames = st.number_input("Enter Number of Frames",min_value=1,max_value=6,value=3,step=1)

if st.button("Run Algorithm"):
    if algorithm=="FIFO":
        page_faults,history=fifo_page_replacement(reference_string,num_frames)
    elif algorithm=="LRU":
        page_faults,history=lru_page_replacement(reference_string,num_frames)
    elif algorithm=="MRU":
        page_faults,history=mru_page_replacement(reference_string,num_frames)
    elif algorithm=="Optimal":
        page_faults,history=optimal_page_replacement(reference_string,num_frames)

    st.write(f"Total Page Faults: {page_faults}")
    
    st.subheader("Frame Status at Each Step")
    frame_table=[]
    for i,frame in enumerate(history):
        frame_table.append([reference_string[i]]+frame+['']*(num_frames-len(frame)))
    
    column_names=["Page References"]+[f"Frame {i+1}" for i in range(num_frames)]
    transposed_table=list(map(list,zip(*([column_names]+frame_table))))
    transposed_table[1:]=transposed_table[1:][::-1]  
    st.table(transposed_table)
