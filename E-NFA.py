'''
10. 正则表达式匹配
困难
相关标签
相关企业
给你一个字符串 s 和一个字符规律 p，请你来实现一个支持 '.' 和 '*' 的正则表达式匹配。

'.' 匹配任意单个字符
'*' 匹配零个或多个前面的那一个元素
所谓匹配，是要涵盖 整个 字符串 s的，而不是部分字符串。

 
示例 1：

输入：s = "aa", p = "a"
输出：false
解释："a" 无法匹配 "aa" 整个字符串。
示例 2:

输入：s = "aa", p = "a*"
输出：true
解释：因为 '*' 代表可以匹配零个或多个前面的那一个元素, 在这里前面的元素就是 'a'。因此，字符串 "aa" 可被视为 'a' 重复了一次。
示例 3：

输入：s = "ab", p = ".*"
输出：true
解释：".*" 表示可匹配零个或多个（'*'）任意字符（'.'）。
'''

def get_epsilon_closure(dict,states):
    checked={}
    new_states=states
    while len(new_states)>0:
        temp=set()
        for state in new_states:
            if(checked.get(state,False)==False and (state,'$') in dict):
                temp.update(dict[(state,'$')])
                checked[state]=True
        new_states=temp
        states.update(new_states)
    return states
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        dict={}
        cur_state=0
        i=0
        # 首先构造ε-NFA
        while i<len(p):
            if(i+1>=len(p) or p[i+1]!='*'):
                dict[(cur_state,p[i])]=[cur_state+1]
                cur_state+=1
            else:
                dict[(cur_state,'$')]=[cur_state+1,cur_state+2]
                dict[(cur_state+1,p[i])]=[cur_state+1]
                dict[(cur_state+1,'$')]=[cur_state+2]
                i+=1
                cur_state+=2
            i+=1
        end_state=cur_state
        # 然后用S跑ε-NFA
        cur_state=get_epsilon_closure(dict,{0})
        for i in range(len(s)):
            next_state=set()
            for state in cur_state:
                if((state,s[i]) in dict or (state,'.') in dict):
                    if((state,s[i]) in dict):
                        next_state.update(dict[(state,s[i])])
                    else:
                        next_state.update(dict[(state,'.')])
            if(len(next_state)==0):
                return False
            cur_state=get_epsilon_closure(dict,next_state)
        if(end_state in cur_state):
            return True
        return False

