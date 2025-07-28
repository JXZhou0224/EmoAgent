from pydantic import BaseModel, Field

# rewrite Event and Timeline class to support pydantic
class Event(BaseModel):
    time: str = Field(default="")
    place: str = Field(default="")
    character: list[str] = Field(default_factory=list)
    summary: str = Field(default="")
    reaction: str = Field(default="")
    original_text_start: int = Field(default=-1)
    original_text_end: int = Field(default=-1)

    def __hash__(self):
        return hash((self.time,self.place,self.summary,self.reaction))
    
    def __eq__(self,other):
        if not isinstance(other,Event):
            return Exception(f"Event and {type(other)} are not comparable")
        return (self.time,self.place,self.summary,self.reaction) == (other.time,other.place,other.summary,other.reaction)
class Timeline(BaseModel):
    '''
    a DAG model, node are events, each event should be assigned with an unique event code
    
    need to support:
    - current time
    - traverse to event
    '''
    init_event: Event = Field(default_factory=lambda: Event(time="init_event"))
    final_event: Event = Field(default_factory=lambda: Event(time="final_event"))
    events: set[Event] = Field(default_factory=lambda: set())
    edges: dict[Event, set[Event]] = Field(default_factory=lambda: {})
    pre_edges: dict[Event, set[Event]] = Field(default_factory=lambda: {})
    
    def __init__(self, **data):
        super().__init__(**data)  # Call the parent class's init
        self.custom_init()

    def custom_init(self):
        self.events.add(self.init_event)
        self.events.add(self.final_event)
        self.edges[self.init_event] = set([self.final_event])
        self.pre_edges[self.final_event] = set([self.init_event])


    def insert_event(self,event: Event, st_event = None,ed_event = None):
        if(st_event is None):
            st_event = self.init_event
        if(ed_event is None):
            ed_event = self.final_event
        if (st_event not in self.events) or (ed_event not in self.events):
            print(self.events)
            raise Exception("Invalid insert, st/ed event not in timeline")

        self.edges[event] = set()
        self.pre_edges[event] = set()
        self.events.add(event)

        if ed_event in self.edges[st_event]:
            self.edges[st_event].remove(ed_event)
            self.pre_edges[ed_event].remove(st_event)

        self.pre_edges[ed_event].add(event)
        self.edges[st_event].add(event)
        return

    def get_init_event(self):
        return self.init_event
    
    def get_final_event(self):
        return self.final_event

    def get_pre(self,event:Event) -> set[Event]:
        return self.pre_edges[event]
    
    def get_after(self,event:Event) -> set[Event]:
        return self.edges[event]
    
    def get_open_timeline(self,event:Event) -> set[Event]:
        return self.get_pre(self.final_event)

    