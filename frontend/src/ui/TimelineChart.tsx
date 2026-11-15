import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

type DayCount = { date: string; count: number };

export default function TimelineChart({ data }: { data: DayCount[] }) {
  return <ResponsiveContainer width="100%" height="100%"><AreaChart data={data} margin={{top:10,right:5,left:-22,bottom:0}}><defs><linearGradient id="greenFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#d6fa72" stopOpacity={0.26}/><stop offset="95%" stopColor="#d6fa72" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#25312c" strokeDasharray="3 5" vertical={false}/><XAxis dataKey="date" stroke="#69766f" tickLine={false} axisLine={false} tick={{fontSize:10}} tickFormatter={v=>new Date(`${v}T12:00:00`).toLocaleDateString('en',{month:'short',day:'numeric'})} interval="preserveStartEnd"/><YAxis stroke="#69766f" tickLine={false} axisLine={false} tick={{fontSize:10}} allowDecimals={false}/><Tooltip contentStyle={{background:'#17221c',border:'1px solid #344239',borderRadius:8,color:'#eef1e9',fontSize:12}} labelFormatter={v=>String(v)} formatter={(v)=>[`${v} records`,'Selected records']}/><Area type="monotone" dataKey="count" stroke="#d6fa72" strokeWidth={2} fill="url(#greenFill)" activeDot={{r:4,fill:'#d6fa72',stroke:'#18231c',strokeWidth:2}}/></AreaChart></ResponsiveContainer>;
}
